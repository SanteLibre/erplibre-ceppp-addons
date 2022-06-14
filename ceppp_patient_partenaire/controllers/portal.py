from collections import OrderedDict
from operator import itemgetter

from odoo import _, http
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.addons.portal.controllers.portal import pager as portal_pager
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from odoo.osv.expression import OR
from odoo.tools import groupby as groupbyelem


class CepppPatientPartenaireController(CustomerPortal):
    def _prepare_portal_layout_values(self):
        values = super(
            CepppPatientPartenaireController, self
        )._prepare_portal_layout_values()
        values["res_partner_count"] = request.env["res.partner"].search_count(
            []
        )
        values["ceppp_chapitre_maladie_count"] = request.env[
            "ceppp.chapitre_maladie"
        ].search_count([])
        values["ceppp_competence_count"] = request.env[
            "ceppp.competence"
        ].search_count([])
        values["ceppp_disponibilite_count"] = request.env[
            "ceppp.disponibilite"
        ].search_count([])
        values["ceppp_formation_count"] = request.env[
            "ceppp.formation"
        ].search_count([])
        values["ceppp_formation_titre_count"] = request.env[
            "ceppp.formation_titre"
        ].search_count([])
        values["ceppp_implication_count"] = request.env[
            "ceppp.implication"
        ].search_count([])
        values["ceppp_implication_domaine_count"] = request.env[
            "ceppp.implication_domaine"
        ].search_count([])
        values["ceppp_implication_role_count"] = request.env[
            "ceppp.implication_role"
        ].search_count([])
        values["ceppp_langue_count"] = request.env[
            "ceppp.langue"
        ].search_count([])
        values["ceppp_maladie_count"] = request.env[
            "ceppp.maladie"
        ].search_count([])
        values["ceppp_maladie_proche_aidant_count"] = request.env[
            "ceppp.maladie_proche_aidant"
        ].search_count([])
        values["ceppp_mode_communication_privilegie_count"] = request.env[
            "ceppp.mode_communication_privilegie"
        ].search_count([])
        values["ceppp_occupation_count"] = request.env[
            "ceppp.occupation"
        ].search_count([])
        values["ceppp_patient_count"] = request.env[
            "ceppp.patient"
        ].search_count([])
        values["ceppp_recruteur_count"] = request.env[
            "ceppp.recruteur"
        ].search_count([])
        values["ceppp_relation_proche_count"] = request.env[
            "ceppp.relation_proche"
        ].search_count([])
        return values

    # ------------------------------------------------------------
    # My Res Partner
    # ------------------------------------------------------------
    def _res_partner_get_page_view_values(
        self, res_partner, access_token, **kwargs
    ):
        values = {
            "page_name": "res_partner",
            "res_partner": res_partner,
            "user": request.env.user,
        }
        return self._get_page_view_values(
            res_partner,
            access_token,
            values,
            "my_res_partners_history",
            False,
            **kwargs,
        )

    @http.route(
        ["/my/res_partners", "/my/res_partners/page/<int:page>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_res_partners(
        self,
        page=1,
        date_begin=None,
        date_end=None,
        sortby=None,
        filterby=None,
        search=None,
        search_in="content",
        **kw,
    ):
        values = self._prepare_portal_layout_values()
        ResPartner = request.env["res.partner"]
        domain = []

        searchbar_sortings = {
            "date": {"label": _("Newest"), "order": "create_date desc"},
            "name": {"label": _("Name"), "order": "name"},
        }
        searchbar_filters = {
            "all": {"label": _("All"), "domain": []},
        }
        searchbar_inputs = {}
        searchbar_groupby = {}

        # default sort by value
        if not sortby:
            sortby = "date"
        order = searchbar_sortings[sortby]["order"]
        # default filter by value
        if not filterby:
            filterby = "all"
        domain = searchbar_filters[filterby]["domain"]

        # search
        if search and search_in:
            search_domain = []
            domain += search_domain
        # archive groups - Default Group By 'create_date'
        archive_groups = self._get_archive_groups("res.partner", domain)
        if date_begin and date_end:
            domain += [
                ("create_date", ">", date_begin),
                ("create_date", "<=", date_end),
            ]
        # res_partners count
        res_partner_count = ResPartner.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/res_partners",
            url_args={
                "date_begin": date_begin,
                "date_end": date_end,
                "sortby": sortby,
                "filterby": filterby,
                "search_in": search_in,
                "search": search,
            },
            total=res_partner_count,
            page=page,
            step=self._items_per_page,
        )

        # content according to pager and archive selected
        res_partners = ResPartner.search(
            domain,
            order=order,
            limit=self._items_per_page,
            offset=pager["offset"],
        )
        request.session["my_res_partners_history"] = res_partners.ids[:100]

        values.update(
            {
                "date": date_begin,
                "date_end": date_end,
                "res_partners": res_partners,
                "page_name": "res_partner",
                "archive_groups": archive_groups,
                "default_url": "/my/res_partners",
                "pager": pager,
                "searchbar_sortings": searchbar_sortings,
                "searchbar_groupby": searchbar_groupby,
                "searchbar_inputs": searchbar_inputs,
                "search_in": search_in,
                "searchbar_filters": OrderedDict(
                    sorted(searchbar_filters.items())
                ),
                "sortby": sortby,
                "filterby": filterby,
            }
        )
        return request.render(
            "ceppp_patient_partenaire.portal_my_res_partners", values
        )

    @http.route(
        ["/my/res_partner/<int:res_partner_id>"],
        type="http",
        auth="public",
        website=True,
    )
    def portal_my_res_partner(
        self, res_partner_id=None, access_token=None, **kw
    ):
        try:
            res_partner_sudo = self._document_check_access(
                "res.partner", res_partner_id, access_token
            )
        except (AccessError, MissingError):
            return request.redirect("/my")

        values = self._res_partner_get_page_view_values(
            res_partner_sudo, access_token, **kw
        )
        return request.render(
            "ceppp_patient_partenaire.portal_my_res_partner", values
        )

    # ------------------------------------------------------------
    # My Ceppp Chapitre_Maladie
    # ------------------------------------------------------------
    def _ceppp_chapitre_maladie_get_page_view_values(
        self, ceppp_chapitre_maladie, access_token, **kwargs
    ):
        values = {
            "page_name": "ceppp_chapitre_maladie",
            "ceppp_chapitre_maladie": ceppp_chapitre_maladie,
            "user": request.env.user,
        }
        return self._get_page_view_values(
            ceppp_chapitre_maladie,
            access_token,
            values,
            "my_ceppp_chapitre_maladies_history",
            False,
            **kwargs,
        )

    @http.route(
        [
            "/my/ceppp_chapitre_maladies",
            "/my/ceppp_chapitre_maladies/page/<int:page>",
        ],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_ceppp_chapitre_maladies(
        self,
        page=1,
        date_begin=None,
        date_end=None,
        sortby=None,
        filterby=None,
        search=None,
        search_in="content",
        **kw,
    ):
        values = self._prepare_portal_layout_values()
        CepppChapitreMaladie = request.env["ceppp.chapitre_maladie"]
        domain = []

        searchbar_sortings = {
            "date": {"label": _("Newest"), "order": "create_date desc"},
            "name": {"label": _("Name"), "order": "name"},
        }
        searchbar_filters = {
            "all": {"label": _("All"), "domain": []},
        }
        searchbar_inputs = {}
        searchbar_groupby = {}

        # default sort by value
        if not sortby:
            sortby = "date"
        order = searchbar_sortings[sortby]["order"]
        # default filter by value
        if not filterby:
            filterby = "all"
        domain = searchbar_filters[filterby]["domain"]

        # search
        if search and search_in:
            search_domain = []
            domain += search_domain
        # archive groups - Default Group By 'create_date'
        archive_groups = self._get_archive_groups(
            "ceppp.chapitre_maladie", domain
        )
        if date_begin and date_end:
            domain += [
                ("create_date", ">", date_begin),
                ("create_date", "<=", date_end),
            ]
        # ceppp_chapitre_maladies count
        ceppp_chapitre_maladie_count = CepppChapitreMaladie.search_count(
            domain
        )
        # pager
        pager = portal_pager(
            url="/my/ceppp_chapitre_maladies",
            url_args={
                "date_begin": date_begin,
                "date_end": date_end,
                "sortby": sortby,
                "filterby": filterby,
                "search_in": search_in,
                "search": search,
            },
            total=ceppp_chapitre_maladie_count,
            page=page,
            step=self._items_per_page,
        )

        # content according to pager and archive selected
        ceppp_chapitre_maladies = CepppChapitreMaladie.search(
            domain,
            order=order,
            limit=self._items_per_page,
            offset=pager["offset"],
        )
        request.session[
            "my_ceppp_chapitre_maladies_history"
        ] = ceppp_chapitre_maladies.ids[:100]

        values.update(
            {
                "date": date_begin,
                "date_end": date_end,
                "ceppp_chapitre_maladies": ceppp_chapitre_maladies,
                "page_name": "ceppp_chapitre_maladie",
                "archive_groups": archive_groups,
                "default_url": "/my/ceppp_chapitre_maladies",
                "pager": pager,
                "searchbar_sortings": searchbar_sortings,
                "searchbar_groupby": searchbar_groupby,
                "searchbar_inputs": searchbar_inputs,
                "search_in": search_in,
                "searchbar_filters": OrderedDict(
                    sorted(searchbar_filters.items())
                ),
                "sortby": sortby,
                "filterby": filterby,
            }
        )
        return request.render(
            "ceppp_patient_partenaire.portal_my_ceppp_chapitre_maladies",
            values,
        )

    @http.route(
        ["/my/ceppp_chapitre_maladie/<int:ceppp_chapitre_maladie_id>"],
        type="http",
        auth="public",
        website=True,
    )
    def portal_my_ceppp_chapitre_maladie(
        self, ceppp_chapitre_maladie_id=None, access_token=None, **kw
    ):
        try:
            ceppp_chapitre_maladie_sudo = self._document_check_access(
                "ceppp.chapitre_maladie",
                ceppp_chapitre_maladie_id,
                access_token,
            )
        except (AccessError, MissingError):
            return request.redirect("/my")

        values = self._ceppp_chapitre_maladie_get_page_view_values(
            ceppp_chapitre_maladie_sudo, access_token, **kw
        )
        return request.render(
            "ceppp_patient_partenaire.portal_my_ceppp_chapitre_maladie", values
        )

    # ------------------------------------------------------------
    # My Ceppp Competence
    # ------------------------------------------------------------
    def _ceppp_competence_get_page_view_values(
        self, ceppp_competence, access_token, **kwargs
    ):
        values = {
            "page_name": "ceppp_competence",
            "ceppp_competence": ceppp_competence,
            "user": request.env.user,
        }
        return self._get_page_view_values(
            ceppp_competence,
            access_token,
            values,
            "my_ceppp_competences_history",
            False,
            **kwargs,
        )

    @http.route(
        ["/my/ceppp_competences", "/my/ceppp_competences/page/<int:page>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_ceppp_competences(
        self,
        page=1,
        date_begin=None,
        date_end=None,
        sortby=None,
        filterby=None,
        search=None,
        search_in="content",
        **kw,
    ):
        values = self._prepare_portal_layout_values()
        CepppCompetence = request.env["ceppp.competence"]
        domain = []

        searchbar_sortings = {
            "date": {"label": _("Newest"), "order": "create_date desc"},
            "name": {"label": _("Name"), "order": "name"},
        }
        searchbar_filters = {
            "all": {"label": _("All"), "domain": []},
        }
        searchbar_inputs = {}
        searchbar_groupby = {}

        # default sort by value
        if not sortby:
            sortby = "date"
        order = searchbar_sortings[sortby]["order"]
        # default filter by value
        if not filterby:
            filterby = "all"
        domain = searchbar_filters[filterby]["domain"]

        # search
        if search and search_in:
            search_domain = []
            domain += search_domain
        # archive groups - Default Group By 'create_date'
        archive_groups = self._get_archive_groups("ceppp.competence", domain)
        if date_begin and date_end:
            domain += [
                ("create_date", ">", date_begin),
                ("create_date", "<=", date_end),
            ]
        # ceppp_competences count
        ceppp_competence_count = CepppCompetence.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/ceppp_competences",
            url_args={
                "date_begin": date_begin,
                "date_end": date_end,
                "sortby": sortby,
                "filterby": filterby,
                "search_in": search_in,
                "search": search,
            },
            total=ceppp_competence_count,
            page=page,
            step=self._items_per_page,
        )

        # content according to pager and archive selected
        ceppp_competences = CepppCompetence.search(
            domain,
            order=order,
            limit=self._items_per_page,
            offset=pager["offset"],
        )
        request.session[
            "my_ceppp_competences_history"
        ] = ceppp_competences.ids[:100]

        values.update(
            {
                "date": date_begin,
                "date_end": date_end,
                "ceppp_competences": ceppp_competences,
                "page_name": "ceppp_competence",
                "archive_groups": archive_groups,
                "default_url": "/my/ceppp_competences",
                "pager": pager,
                "searchbar_sortings": searchbar_sortings,
                "searchbar_groupby": searchbar_groupby,
                "searchbar_inputs": searchbar_inputs,
                "search_in": search_in,
                "searchbar_filters": OrderedDict(
                    sorted(searchbar_filters.items())
                ),
                "sortby": sortby,
                "filterby": filterby,
            }
        )
        return request.render(
            "ceppp_patient_partenaire.portal_my_ceppp_competences", values
        )

    @http.route(
        ["/my/ceppp_competence/<int:ceppp_competence_id>"],
        type="http",
        auth="public",
        website=True,
    )
    def portal_my_ceppp_competence(
        self, ceppp_competence_id=None, access_token=None, **kw
    ):
        try:
            ceppp_competence_sudo = self._document_check_access(
                "ceppp.competence", ceppp_competence_id, access_token
            )
        except (AccessError, MissingError):
            return request.redirect("/my")

        values = self._ceppp_competence_get_page_view_values(
            ceppp_competence_sudo, access_token, **kw
        )
        return request.render(
            "ceppp_patient_partenaire.portal_my_ceppp_competence", values
        )

    # ------------------------------------------------------------
    # My Ceppp Disponibilite
    # ------------------------------------------------------------
    def _ceppp_disponibilite_get_page_view_values(
        self, ceppp_disponibilite, access_token, **kwargs
    ):
        values = {
            "page_name": "ceppp_disponibilite",
            "ceppp_disponibilite": ceppp_disponibilite,
            "user": request.env.user,
        }
        return self._get_page_view_values(
            ceppp_disponibilite,
            access_token,
            values,
            "my_ceppp_disponibilites_history",
            False,
            **kwargs,
        )

    @http.route(
        [
            "/my/ceppp_disponibilites",
            "/my/ceppp_disponibilites/page/<int:page>",
        ],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_ceppp_disponibilites(
        self,
        page=1,
        date_begin=None,
        date_end=None,
        sortby=None,
        filterby=None,
        search=None,
        search_in="content",
        **kw,
    ):
        values = self._prepare_portal_layout_values()
        CepppDisponibilite = request.env["ceppp.disponibilite"]
        domain = []

        searchbar_sortings = {
            "date": {"label": _("Newest"), "order": "create_date desc"},
            "name": {"label": _("Name"), "order": "name"},
        }
        searchbar_filters = {
            "all": {"label": _("All"), "domain": []},
        }
        searchbar_inputs = {}
        searchbar_groupby = {}

        # default sort by value
        if not sortby:
            sortby = "date"
        order = searchbar_sortings[sortby]["order"]
        # default filter by value
        if not filterby:
            filterby = "all"
        domain = searchbar_filters[filterby]["domain"]

        # search
        if search and search_in:
            search_domain = []
            domain += search_domain
        # archive groups - Default Group By 'create_date'
        archive_groups = self._get_archive_groups(
            "ceppp.disponibilite", domain
        )
        if date_begin and date_end:
            domain += [
                ("create_date", ">", date_begin),
                ("create_date", "<=", date_end),
            ]
        # ceppp_disponibilites count
        ceppp_disponibilite_count = CepppDisponibilite.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/ceppp_disponibilites",
            url_args={
                "date_begin": date_begin,
                "date_end": date_end,
                "sortby": sortby,
                "filterby": filterby,
                "search_in": search_in,
                "search": search,
            },
            total=ceppp_disponibilite_count,
            page=page,
            step=self._items_per_page,
        )

        # content according to pager and archive selected
        ceppp_disponibilites = CepppDisponibilite.search(
            domain,
            order=order,
            limit=self._items_per_page,
            offset=pager["offset"],
        )
        request.session[
            "my_ceppp_disponibilites_history"
        ] = ceppp_disponibilites.ids[:100]

        values.update(
            {
                "date": date_begin,
                "date_end": date_end,
                "ceppp_disponibilites": ceppp_disponibilites,
                "page_name": "ceppp_disponibilite",
                "archive_groups": archive_groups,
                "default_url": "/my/ceppp_disponibilites",
                "pager": pager,
                "searchbar_sortings": searchbar_sortings,
                "searchbar_groupby": searchbar_groupby,
                "searchbar_inputs": searchbar_inputs,
                "search_in": search_in,
                "searchbar_filters": OrderedDict(
                    sorted(searchbar_filters.items())
                ),
                "sortby": sortby,
                "filterby": filterby,
            }
        )
        return request.render(
            "ceppp_patient_partenaire.portal_my_ceppp_disponibilites", values
        )

    @http.route(
        ["/my/ceppp_disponibilite/<int:ceppp_disponibilite_id>"],
        type="http",
        auth="public",
        website=True,
    )
    def portal_my_ceppp_disponibilite(
        self, ceppp_disponibilite_id=None, access_token=None, **kw
    ):
        try:
            ceppp_disponibilite_sudo = self._document_check_access(
                "ceppp.disponibilite", ceppp_disponibilite_id, access_token
            )
        except (AccessError, MissingError):
            return request.redirect("/my")

        values = self._ceppp_disponibilite_get_page_view_values(
            ceppp_disponibilite_sudo, access_token, **kw
        )
        return request.render(
            "ceppp_patient_partenaire.portal_my_ceppp_disponibilite", values
        )

    # ------------------------------------------------------------
    # My Ceppp Formation
    # ------------------------------------------------------------
    def _ceppp_formation_get_page_view_values(
        self, ceppp_formation, access_token, **kwargs
    ):
        values = {
            "page_name": "ceppp_formation",
            "ceppp_formation": ceppp_formation,
            "user": request.env.user,
        }
        return self._get_page_view_values(
            ceppp_formation,
            access_token,
            values,
            "my_ceppp_formations_history",
            False,
            **kwargs,
        )

    @http.route(
        ["/my/ceppp_formations", "/my/ceppp_formations/page/<int:page>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_ceppp_formations(
        self,
        page=1,
        date_begin=None,
        date_end=None,
        sortby=None,
        filterby=None,
        search=None,
        search_in="content",
        **kw,
    ):
        values = self._prepare_portal_layout_values()
        CepppFormation = request.env["ceppp.formation"]
        domain = []

        searchbar_sortings = {
            "date": {"label": _("Newest"), "order": "create_date desc"},
            "name": {"label": _("Name"), "order": "name"},
        }
        searchbar_filters = {
            "all": {"label": _("All"), "domain": []},
        }
        searchbar_inputs = {}
        searchbar_groupby = {}

        # default sort by value
        if not sortby:
            sortby = "date"
        order = searchbar_sortings[sortby]["order"]
        # default filter by value
        if not filterby:
            filterby = "all"
        domain = searchbar_filters[filterby]["domain"]

        # search
        if search and search_in:
            search_domain = []
            domain += search_domain
        # archive groups - Default Group By 'create_date'
        archive_groups = self._get_archive_groups("ceppp.formation", domain)
        if date_begin and date_end:
            domain += [
                ("create_date", ">", date_begin),
                ("create_date", "<=", date_end),
            ]
        # ceppp_formations count
        ceppp_formation_count = CepppFormation.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/ceppp_formations",
            url_args={
                "date_begin": date_begin,
                "date_end": date_end,
                "sortby": sortby,
                "filterby": filterby,
                "search_in": search_in,
                "search": search,
            },
            total=ceppp_formation_count,
            page=page,
            step=self._items_per_page,
        )

        # content according to pager and archive selected
        ceppp_formations = CepppFormation.search(
            domain,
            order=order,
            limit=self._items_per_page,
            offset=pager["offset"],
        )
        request.session["my_ceppp_formations_history"] = ceppp_formations.ids[
            :100
        ]

        values.update(
            {
                "date": date_begin,
                "date_end": date_end,
                "ceppp_formations": ceppp_formations,
                "page_name": "ceppp_formation",
                "archive_groups": archive_groups,
                "default_url": "/my/ceppp_formations",
                "pager": pager,
                "searchbar_sortings": searchbar_sortings,
                "searchbar_groupby": searchbar_groupby,
                "searchbar_inputs": searchbar_inputs,
                "search_in": search_in,
                "searchbar_filters": OrderedDict(
                    sorted(searchbar_filters.items())
                ),
                "sortby": sortby,
                "filterby": filterby,
            }
        )
        return request.render(
            "ceppp_patient_partenaire.portal_my_ceppp_formations", values
        )

    @http.route(
        ["/my/ceppp_formation/<int:ceppp_formation_id>"],
        type="http",
        auth="public",
        website=True,
    )
    def portal_my_ceppp_formation(
        self, ceppp_formation_id=None, access_token=None, **kw
    ):
        try:
            ceppp_formation_sudo = self._document_check_access(
                "ceppp.formation", ceppp_formation_id, access_token
            )
        except (AccessError, MissingError):
            return request.redirect("/my")

        values = self._ceppp_formation_get_page_view_values(
            ceppp_formation_sudo, access_token, **kw
        )
        return request.render(
            "ceppp_patient_partenaire.portal_my_ceppp_formation", values
        )

    # ------------------------------------------------------------
    # My Ceppp Formation_Titre
    # ------------------------------------------------------------
    def _ceppp_formation_titre_get_page_view_values(
        self, ceppp_formation_titre, access_token, **kwargs
    ):
        values = {
            "page_name": "ceppp_formation_titre",
            "ceppp_formation_titre": ceppp_formation_titre,
            "user": request.env.user,
        }
        return self._get_page_view_values(
            ceppp_formation_titre,
            access_token,
            values,
            "my_ceppp_formation_titres_history",
            False,
            **kwargs,
        )

    @http.route(
        [
            "/my/ceppp_formation_titres",
            "/my/ceppp_formation_titres/page/<int:page>",
        ],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_ceppp_formation_titres(
        self,
        page=1,
        date_begin=None,
        date_end=None,
        sortby=None,
        filterby=None,
        search=None,
        search_in="content",
        **kw,
    ):
        values = self._prepare_portal_layout_values()
        CepppFormationTitre = request.env["ceppp.formation_titre"]
        domain = []

        searchbar_sortings = {
            "date": {"label": _("Newest"), "order": "create_date desc"},
            "name": {"label": _("Name"), "order": "name"},
        }
        searchbar_filters = {
            "all": {"label": _("All"), "domain": []},
        }
        searchbar_inputs = {}
        searchbar_groupby = {}

        # default sort by value
        if not sortby:
            sortby = "date"
        order = searchbar_sortings[sortby]["order"]
        # default filter by value
        if not filterby:
            filterby = "all"
        domain = searchbar_filters[filterby]["domain"]

        # search
        if search and search_in:
            search_domain = []
            domain += search_domain
        # archive groups - Default Group By 'create_date'
        archive_groups = self._get_archive_groups(
            "ceppp.formation_titre", domain
        )
        if date_begin and date_end:
            domain += [
                ("create_date", ">", date_begin),
                ("create_date", "<=", date_end),
            ]
        # ceppp_formation_titres count
        ceppp_formation_titre_count = CepppFormationTitre.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/ceppp_formation_titres",
            url_args={
                "date_begin": date_begin,
                "date_end": date_end,
                "sortby": sortby,
                "filterby": filterby,
                "search_in": search_in,
                "search": search,
            },
            total=ceppp_formation_titre_count,
            page=page,
            step=self._items_per_page,
        )

        # content according to pager and archive selected
        ceppp_formation_titres = CepppFormationTitre.search(
            domain,
            order=order,
            limit=self._items_per_page,
            offset=pager["offset"],
        )
        request.session[
            "my_ceppp_formation_titres_history"
        ] = ceppp_formation_titres.ids[:100]

        values.update(
            {
                "date": date_begin,
                "date_end": date_end,
                "ceppp_formation_titres": ceppp_formation_titres,
                "page_name": "ceppp_formation_titre",
                "archive_groups": archive_groups,
                "default_url": "/my/ceppp_formation_titres",
                "pager": pager,
                "searchbar_sortings": searchbar_sortings,
                "searchbar_groupby": searchbar_groupby,
                "searchbar_inputs": searchbar_inputs,
                "search_in": search_in,
                "searchbar_filters": OrderedDict(
                    sorted(searchbar_filters.items())
                ),
                "sortby": sortby,
                "filterby": filterby,
            }
        )
        return request.render(
            "ceppp_patient_partenaire.portal_my_ceppp_formation_titres", values
        )

    @http.route(
        ["/my/ceppp_formation_titre/<int:ceppp_formation_titre_id>"],
        type="http",
        auth="public",
        website=True,
    )
    def portal_my_ceppp_formation_titre(
        self, ceppp_formation_titre_id=None, access_token=None, **kw
    ):
        try:
            ceppp_formation_titre_sudo = self._document_check_access(
                "ceppp.formation_titre", ceppp_formation_titre_id, access_token
            )
        except (AccessError, MissingError):
            return request.redirect("/my")

        values = self._ceppp_formation_titre_get_page_view_values(
            ceppp_formation_titre_sudo, access_token, **kw
        )
        return request.render(
            "ceppp_patient_partenaire.portal_my_ceppp_formation_titre", values
        )

    # ------------------------------------------------------------
    # My Ceppp Implication
    # ------------------------------------------------------------
    def _ceppp_implication_get_page_view_values(
        self, ceppp_implication, access_token, **kwargs
    ):
        values = {
            "page_name": "ceppp_implication",
            "ceppp_implication": ceppp_implication,
            "user": request.env.user,
        }
        return self._get_page_view_values(
            ceppp_implication,
            access_token,
            values,
            "my_ceppp_implications_history",
            False,
            **kwargs,
        )

    @http.route(
        ["/my/ceppp_implications", "/my/ceppp_implications/page/<int:page>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_ceppp_implications(
        self,
        page=1,
        date_begin=None,
        date_end=None,
        sortby=None,
        filterby=None,
        search=None,
        search_in="content",
        **kw,
    ):
        values = self._prepare_portal_layout_values()
        CepppImplication = request.env["ceppp.implication"]
        domain = []

        searchbar_sortings = {
            "date": {"label": _("Newest"), "order": "create_date desc"},
            "name": {"label": _("Name"), "order": "name"},
        }
        searchbar_filters = {
            "all": {"label": _("All"), "domain": []},
        }
        searchbar_inputs = {}
        searchbar_groupby = {}

        # default sort by value
        if not sortby:
            sortby = "date"
        order = searchbar_sortings[sortby]["order"]
        # default filter by value
        if not filterby:
            filterby = "all"
        domain = searchbar_filters[filterby]["domain"]

        # search
        if search and search_in:
            search_domain = []
            domain += search_domain
        # archive groups - Default Group By 'create_date'
        archive_groups = self._get_archive_groups("ceppp.implication", domain)
        if date_begin and date_end:
            domain += [
                ("create_date", ">", date_begin),
                ("create_date", "<=", date_end),
            ]
        # ceppp_implications count
        ceppp_implication_count = CepppImplication.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/ceppp_implications",
            url_args={
                "date_begin": date_begin,
                "date_end": date_end,
                "sortby": sortby,
                "filterby": filterby,
                "search_in": search_in,
                "search": search,
            },
            total=ceppp_implication_count,
            page=page,
            step=self._items_per_page,
        )

        # content according to pager and archive selected
        ceppp_implications = CepppImplication.search(
            domain,
            order=order,
            limit=self._items_per_page,
            offset=pager["offset"],
        )
        request.session[
            "my_ceppp_implications_history"
        ] = ceppp_implications.ids[:100]

        values.update(
            {
                "date": date_begin,
                "date_end": date_end,
                "ceppp_implications": ceppp_implications,
                "page_name": "ceppp_implication",
                "archive_groups": archive_groups,
                "default_url": "/my/ceppp_implications",
                "pager": pager,
                "searchbar_sortings": searchbar_sortings,
                "searchbar_groupby": searchbar_groupby,
                "searchbar_inputs": searchbar_inputs,
                "search_in": search_in,
                "searchbar_filters": OrderedDict(
                    sorted(searchbar_filters.items())
                ),
                "sortby": sortby,
                "filterby": filterby,
            }
        )
        return request.render(
            "ceppp_patient_partenaire.portal_my_ceppp_implications", values
        )

    @http.route(
        ["/my/ceppp_implication/<int:ceppp_implication_id>"],
        type="http",
        auth="public",
        website=True,
    )
    def portal_my_ceppp_implication(
        self, ceppp_implication_id=None, access_token=None, **kw
    ):
        try:
            ceppp_implication_sudo = self._document_check_access(
                "ceppp.implication", ceppp_implication_id, access_token
            )
        except (AccessError, MissingError):
            return request.redirect("/my")

        values = self._ceppp_implication_get_page_view_values(
            ceppp_implication_sudo, access_token, **kw
        )
        return request.render(
            "ceppp_patient_partenaire.portal_my_ceppp_implication", values
        )

    # ------------------------------------------------------------
    # My Ceppp Implication_Domaine
    # ------------------------------------------------------------
    def _ceppp_implication_domaine_get_page_view_values(
        self, ceppp_implication_domaine, access_token, **kwargs
    ):
        values = {
            "page_name": "ceppp_implication_domaine",
            "ceppp_implication_domaine": ceppp_implication_domaine,
            "user": request.env.user,
        }
        return self._get_page_view_values(
            ceppp_implication_domaine,
            access_token,
            values,
            "my_ceppp_implication_domaines_history",
            False,
            **kwargs,
        )

    @http.route(
        [
            "/my/ceppp_implication_domaines",
            "/my/ceppp_implication_domaines/page/<int:page>",
        ],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_ceppp_implication_domaines(
        self,
        page=1,
        date_begin=None,
        date_end=None,
        sortby=None,
        filterby=None,
        search=None,
        search_in="content",
        **kw,
    ):
        values = self._prepare_portal_layout_values()
        CepppImplicationDomaine = request.env["ceppp.implication_domaine"]
        domain = []

        searchbar_sortings = {
            "date": {"label": _("Newest"), "order": "create_date desc"},
            "name": {"label": _("Name"), "order": "name"},
        }
        searchbar_filters = {
            "all": {"label": _("All"), "domain": []},
        }
        searchbar_inputs = {}
        searchbar_groupby = {}

        # default sort by value
        if not sortby:
            sortby = "date"
        order = searchbar_sortings[sortby]["order"]
        # default filter by value
        if not filterby:
            filterby = "all"
        domain = searchbar_filters[filterby]["domain"]

        # search
        if search and search_in:
            search_domain = []
            domain += search_domain
        # archive groups - Default Group By 'create_date'
        archive_groups = self._get_archive_groups(
            "ceppp.implication_domaine", domain
        )
        if date_begin and date_end:
            domain += [
                ("create_date", ">", date_begin),
                ("create_date", "<=", date_end),
            ]
        # ceppp_implication_domaines count
        ceppp_implication_domaine_count = CepppImplicationDomaine.search_count(
            domain
        )
        # pager
        pager = portal_pager(
            url="/my/ceppp_implication_domaines",
            url_args={
                "date_begin": date_begin,
                "date_end": date_end,
                "sortby": sortby,
                "filterby": filterby,
                "search_in": search_in,
                "search": search,
            },
            total=ceppp_implication_domaine_count,
            page=page,
            step=self._items_per_page,
        )

        # content according to pager and archive selected
        ceppp_implication_domaines = CepppImplicationDomaine.search(
            domain,
            order=order,
            limit=self._items_per_page,
            offset=pager["offset"],
        )
        request.session[
            "my_ceppp_implication_domaines_history"
        ] = ceppp_implication_domaines.ids[:100]

        values.update(
            {
                "date": date_begin,
                "date_end": date_end,
                "ceppp_implication_domaines": ceppp_implication_domaines,
                "page_name": "ceppp_implication_domaine",
                "archive_groups": archive_groups,
                "default_url": "/my/ceppp_implication_domaines",
                "pager": pager,
                "searchbar_sortings": searchbar_sortings,
                "searchbar_groupby": searchbar_groupby,
                "searchbar_inputs": searchbar_inputs,
                "search_in": search_in,
                "searchbar_filters": OrderedDict(
                    sorted(searchbar_filters.items())
                ),
                "sortby": sortby,
                "filterby": filterby,
            }
        )
        return request.render(
            "ceppp_patient_partenaire.portal_my_ceppp_implication_domaines",
            values,
        )

    @http.route(
        ["/my/ceppp_implication_domaine/<int:ceppp_implication_domaine_id>"],
        type="http",
        auth="public",
        website=True,
    )
    def portal_my_ceppp_implication_domaine(
        self, ceppp_implication_domaine_id=None, access_token=None, **kw
    ):
        try:
            ceppp_implication_domaine_sudo = self._document_check_access(
                "ceppp.implication_domaine",
                ceppp_implication_domaine_id,
                access_token,
            )
        except (AccessError, MissingError):
            return request.redirect("/my")

        values = self._ceppp_implication_domaine_get_page_view_values(
            ceppp_implication_domaine_sudo, access_token, **kw
        )
        return request.render(
            "ceppp_patient_partenaire.portal_my_ceppp_implication_domaine",
            values,
        )

    # ------------------------------------------------------------
    # My Ceppp Implication_Role
    # ------------------------------------------------------------
    def _ceppp_implication_role_get_page_view_values(
        self, ceppp_implication_role, access_token, **kwargs
    ):
        values = {
            "page_name": "ceppp_implication_role",
            "ceppp_implication_role": ceppp_implication_role,
            "user": request.env.user,
        }
        return self._get_page_view_values(
            ceppp_implication_role,
            access_token,
            values,
            "my_ceppp_implication_roles_history",
            False,
            **kwargs,
        )

    @http.route(
        [
            "/my/ceppp_implication_roles",
            "/my/ceppp_implication_roles/page/<int:page>",
        ],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_ceppp_implication_roles(
        self,
        page=1,
        date_begin=None,
        date_end=None,
        sortby=None,
        filterby=None,
        search=None,
        search_in="content",
        **kw,
    ):
        values = self._prepare_portal_layout_values()
        CepppImplicationRole = request.env["ceppp.implication_role"]
        domain = []

        searchbar_sortings = {
            "date": {"label": _("Newest"), "order": "create_date desc"},
            "name": {"label": _("Name"), "order": "name"},
        }
        searchbar_filters = {
            "all": {"label": _("All"), "domain": []},
        }
        searchbar_inputs = {}
        searchbar_groupby = {}

        # default sort by value
        if not sortby:
            sortby = "date"
        order = searchbar_sortings[sortby]["order"]
        # default filter by value
        if not filterby:
            filterby = "all"
        domain = searchbar_filters[filterby]["domain"]

        # search
        if search and search_in:
            search_domain = []
            domain += search_domain
        # archive groups - Default Group By 'create_date'
        archive_groups = self._get_archive_groups(
            "ceppp.implication_role", domain
        )
        if date_begin and date_end:
            domain += [
                ("create_date", ">", date_begin),
                ("create_date", "<=", date_end),
            ]
        # ceppp_implication_roles count
        ceppp_implication_role_count = CepppImplicationRole.search_count(
            domain
        )
        # pager
        pager = portal_pager(
            url="/my/ceppp_implication_roles",
            url_args={
                "date_begin": date_begin,
                "date_end": date_end,
                "sortby": sortby,
                "filterby": filterby,
                "search_in": search_in,
                "search": search,
            },
            total=ceppp_implication_role_count,
            page=page,
            step=self._items_per_page,
        )

        # content according to pager and archive selected
        ceppp_implication_roles = CepppImplicationRole.search(
            domain,
            order=order,
            limit=self._items_per_page,
            offset=pager["offset"],
        )
        request.session[
            "my_ceppp_implication_roles_history"
        ] = ceppp_implication_roles.ids[:100]

        values.update(
            {
                "date": date_begin,
                "date_end": date_end,
                "ceppp_implication_roles": ceppp_implication_roles,
                "page_name": "ceppp_implication_role",
                "archive_groups": archive_groups,
                "default_url": "/my/ceppp_implication_roles",
                "pager": pager,
                "searchbar_sortings": searchbar_sortings,
                "searchbar_groupby": searchbar_groupby,
                "searchbar_inputs": searchbar_inputs,
                "search_in": search_in,
                "searchbar_filters": OrderedDict(
                    sorted(searchbar_filters.items())
                ),
                "sortby": sortby,
                "filterby": filterby,
            }
        )
        return request.render(
            "ceppp_patient_partenaire.portal_my_ceppp_implication_roles",
            values,
        )

    @http.route(
        ["/my/ceppp_implication_role/<int:ceppp_implication_role_id>"],
        type="http",
        auth="public",
        website=True,
    )
    def portal_my_ceppp_implication_role(
        self, ceppp_implication_role_id=None, access_token=None, **kw
    ):
        try:
            ceppp_implication_role_sudo = self._document_check_access(
                "ceppp.implication_role",
                ceppp_implication_role_id,
                access_token,
            )
        except (AccessError, MissingError):
            return request.redirect("/my")

        values = self._ceppp_implication_role_get_page_view_values(
            ceppp_implication_role_sudo, access_token, **kw
        )
        return request.render(
            "ceppp_patient_partenaire.portal_my_ceppp_implication_role", values
        )

    # ------------------------------------------------------------
    # My Ceppp Langue
    # ------------------------------------------------------------
    def _ceppp_langue_get_page_view_values(
        self, ceppp_langue, access_token, **kwargs
    ):
        values = {
            "page_name": "ceppp_langue",
            "ceppp_langue": ceppp_langue,
            "user": request.env.user,
        }
        return self._get_page_view_values(
            ceppp_langue,
            access_token,
            values,
            "my_ceppp_langues_history",
            False,
            **kwargs,
        )

    @http.route(
        ["/my/ceppp_langues", "/my/ceppp_langues/page/<int:page>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_ceppp_langues(
        self,
        page=1,
        date_begin=None,
        date_end=None,
        sortby=None,
        filterby=None,
        search=None,
        search_in="content",
        **kw,
    ):
        values = self._prepare_portal_layout_values()
        CepppLangue = request.env["ceppp.langue"]
        domain = []

        searchbar_sortings = {
            "date": {"label": _("Newest"), "order": "create_date desc"},
            "name": {"label": _("Name"), "order": "name"},
        }
        searchbar_filters = {
            "all": {"label": _("All"), "domain": []},
        }
        searchbar_inputs = {}
        searchbar_groupby = {}

        # default sort by value
        if not sortby:
            sortby = "date"
        order = searchbar_sortings[sortby]["order"]
        # default filter by value
        if not filterby:
            filterby = "all"
        domain = searchbar_filters[filterby]["domain"]

        # search
        if search and search_in:
            search_domain = []
            domain += search_domain
        # archive groups - Default Group By 'create_date'
        archive_groups = self._get_archive_groups("ceppp.langue", domain)
        if date_begin and date_end:
            domain += [
                ("create_date", ">", date_begin),
                ("create_date", "<=", date_end),
            ]
        # ceppp_langues count
        ceppp_langue_count = CepppLangue.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/ceppp_langues",
            url_args={
                "date_begin": date_begin,
                "date_end": date_end,
                "sortby": sortby,
                "filterby": filterby,
                "search_in": search_in,
                "search": search,
            },
            total=ceppp_langue_count,
            page=page,
            step=self._items_per_page,
        )

        # content according to pager and archive selected
        ceppp_langues = CepppLangue.search(
            domain,
            order=order,
            limit=self._items_per_page,
            offset=pager["offset"],
        )
        request.session["my_ceppp_langues_history"] = ceppp_langues.ids[:100]

        values.update(
            {
                "date": date_begin,
                "date_end": date_end,
                "ceppp_langues": ceppp_langues,
                "page_name": "ceppp_langue",
                "archive_groups": archive_groups,
                "default_url": "/my/ceppp_langues",
                "pager": pager,
                "searchbar_sortings": searchbar_sortings,
                "searchbar_groupby": searchbar_groupby,
                "searchbar_inputs": searchbar_inputs,
                "search_in": search_in,
                "searchbar_filters": OrderedDict(
                    sorted(searchbar_filters.items())
                ),
                "sortby": sortby,
                "filterby": filterby,
            }
        )
        return request.render(
            "ceppp_patient_partenaire.portal_my_ceppp_langues", values
        )

    @http.route(
        ["/my/ceppp_langue/<int:ceppp_langue_id>"],
        type="http",
        auth="public",
        website=True,
    )
    def portal_my_ceppp_langue(
        self, ceppp_langue_id=None, access_token=None, **kw
    ):
        try:
            ceppp_langue_sudo = self._document_check_access(
                "ceppp.langue", ceppp_langue_id, access_token
            )
        except (AccessError, MissingError):
            return request.redirect("/my")

        values = self._ceppp_langue_get_page_view_values(
            ceppp_langue_sudo, access_token, **kw
        )
        return request.render(
            "ceppp_patient_partenaire.portal_my_ceppp_langue", values
        )

    # ------------------------------------------------------------
    # My Ceppp Maladie
    # ------------------------------------------------------------
    def _ceppp_maladie_get_page_view_values(
        self, ceppp_maladie, access_token, **kwargs
    ):
        values = {
            "page_name": "ceppp_maladie",
            "ceppp_maladie": ceppp_maladie,
            "user": request.env.user,
        }
        return self._get_page_view_values(
            ceppp_maladie,
            access_token,
            values,
            "my_ceppp_maladies_history",
            False,
            **kwargs,
        )

    @http.route(
        ["/my/ceppp_maladies", "/my/ceppp_maladies/page/<int:page>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_ceppp_maladies(
        self,
        page=1,
        date_begin=None,
        date_end=None,
        sortby=None,
        filterby=None,
        search=None,
        search_in="content",
        **kw,
    ):
        values = self._prepare_portal_layout_values()
        CepppMaladie = request.env["ceppp.maladie"]
        domain = []

        searchbar_sortings = {
            "date": {"label": _("Newest"), "order": "create_date desc"},
            "name": {"label": _("Name"), "order": "name"},
        }
        searchbar_filters = {
            "all": {"label": _("All"), "domain": []},
        }
        searchbar_inputs = {}
        searchbar_groupby = {}

        # default sort by value
        if not sortby:
            sortby = "date"
        order = searchbar_sortings[sortby]["order"]
        # default filter by value
        if not filterby:
            filterby = "all"
        domain = searchbar_filters[filterby]["domain"]

        # search
        if search and search_in:
            search_domain = []
            domain += search_domain
        # archive groups - Default Group By 'create_date'
        archive_groups = self._get_archive_groups("ceppp.maladie", domain)
        if date_begin and date_end:
            domain += [
                ("create_date", ">", date_begin),
                ("create_date", "<=", date_end),
            ]
        # ceppp_maladies count
        ceppp_maladie_count = CepppMaladie.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/ceppp_maladies",
            url_args={
                "date_begin": date_begin,
                "date_end": date_end,
                "sortby": sortby,
                "filterby": filterby,
                "search_in": search_in,
                "search": search,
            },
            total=ceppp_maladie_count,
            page=page,
            step=self._items_per_page,
        )

        # content according to pager and archive selected
        ceppp_maladies = CepppMaladie.search(
            domain,
            order=order,
            limit=self._items_per_page,
            offset=pager["offset"],
        )
        request.session["my_ceppp_maladies_history"] = ceppp_maladies.ids[:100]

        values.update(
            {
                "date": date_begin,
                "date_end": date_end,
                "ceppp_maladies": ceppp_maladies,
                "page_name": "ceppp_maladie",
                "archive_groups": archive_groups,
                "default_url": "/my/ceppp_maladies",
                "pager": pager,
                "searchbar_sortings": searchbar_sortings,
                "searchbar_groupby": searchbar_groupby,
                "searchbar_inputs": searchbar_inputs,
                "search_in": search_in,
                "searchbar_filters": OrderedDict(
                    sorted(searchbar_filters.items())
                ),
                "sortby": sortby,
                "filterby": filterby,
            }
        )
        return request.render(
            "ceppp_patient_partenaire.portal_my_ceppp_maladies", values
        )

    @http.route(
        ["/my/ceppp_maladie/<int:ceppp_maladie_id>"],
        type="http",
        auth="public",
        website=True,
    )
    def portal_my_ceppp_maladie(
        self, ceppp_maladie_id=None, access_token=None, **kw
    ):
        try:
            ceppp_maladie_sudo = self._document_check_access(
                "ceppp.maladie", ceppp_maladie_id, access_token
            )
        except (AccessError, MissingError):
            return request.redirect("/my")

        values = self._ceppp_maladie_get_page_view_values(
            ceppp_maladie_sudo, access_token, **kw
        )
        return request.render(
            "ceppp_patient_partenaire.portal_my_ceppp_maladie", values
        )

    # ------------------------------------------------------------
    # My Ceppp Maladie_Proche_Aidant
    # ------------------------------------------------------------
    def _ceppp_maladie_proche_aidant_get_page_view_values(
        self, ceppp_maladie_proche_aidant, access_token, **kwargs
    ):
        values = {
            "page_name": "ceppp_maladie_proche_aidant",
            "ceppp_maladie_proche_aidant": ceppp_maladie_proche_aidant,
            "user": request.env.user,
        }
        return self._get_page_view_values(
            ceppp_maladie_proche_aidant,
            access_token,
            values,
            "my_ceppp_maladie_proche_aidants_history",
            False,
            **kwargs,
        )

    @http.route(
        [
            "/my/ceppp_maladie_proche_aidants",
            "/my/ceppp_maladie_proche_aidants/page/<int:page>",
        ],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_ceppp_maladie_proche_aidants(
        self,
        page=1,
        date_begin=None,
        date_end=None,
        sortby=None,
        filterby=None,
        search=None,
        search_in="content",
        **kw,
    ):
        values = self._prepare_portal_layout_values()
        CepppMaladieProcheAidant = request.env["ceppp.maladie_proche_aidant"]
        domain = []

        searchbar_sortings = {
            "date": {"label": _("Newest"), "order": "create_date desc"},
            "name": {"label": _("Name"), "order": "name"},
        }
        searchbar_filters = {
            "all": {"label": _("All"), "domain": []},
        }
        searchbar_inputs = {}
        searchbar_groupby = {}

        # default sort by value
        if not sortby:
            sortby = "date"
        order = searchbar_sortings[sortby]["order"]
        # default filter by value
        if not filterby:
            filterby = "all"
        domain = searchbar_filters[filterby]["domain"]

        # search
        if search and search_in:
            search_domain = []
            domain += search_domain
        # archive groups - Default Group By 'create_date'
        archive_groups = self._get_archive_groups(
            "ceppp.maladie_proche_aidant", domain
        )
        if date_begin and date_end:
            domain += [
                ("create_date", ">", date_begin),
                ("create_date", "<=", date_end),
            ]
        # ceppp_maladie_proche_aidants count
        ceppp_maladie_proche_aidant_count = (
            CepppMaladieProcheAidant.search_count(domain)
        )
        # pager
        pager = portal_pager(
            url="/my/ceppp_maladie_proche_aidants",
            url_args={
                "date_begin": date_begin,
                "date_end": date_end,
                "sortby": sortby,
                "filterby": filterby,
                "search_in": search_in,
                "search": search,
            },
            total=ceppp_maladie_proche_aidant_count,
            page=page,
            step=self._items_per_page,
        )

        # content according to pager and archive selected
        ceppp_maladie_proche_aidants = CepppMaladieProcheAidant.search(
            domain,
            order=order,
            limit=self._items_per_page,
            offset=pager["offset"],
        )
        request.session[
            "my_ceppp_maladie_proche_aidants_history"
        ] = ceppp_maladie_proche_aidants.ids[:100]

        values.update(
            {
                "date": date_begin,
                "date_end": date_end,
                "ceppp_maladie_proche_aidants": ceppp_maladie_proche_aidants,
                "page_name": "ceppp_maladie_proche_aidant",
                "archive_groups": archive_groups,
                "default_url": "/my/ceppp_maladie_proche_aidants",
                "pager": pager,
                "searchbar_sortings": searchbar_sortings,
                "searchbar_groupby": searchbar_groupby,
                "searchbar_inputs": searchbar_inputs,
                "search_in": search_in,
                "searchbar_filters": OrderedDict(
                    sorted(searchbar_filters.items())
                ),
                "sortby": sortby,
                "filterby": filterby,
            }
        )
        return request.render(
            "ceppp_patient_partenaire.portal_my_ceppp_maladie_proche_aidants",
            values,
        )

    @http.route(
        [
            "/my/ceppp_maladie_proche_aidant/<int:ceppp_maladie_proche_aidant_id>"
        ],
        type="http",
        auth="public",
        website=True,
    )
    def portal_my_ceppp_maladie_proche_aidant(
        self, ceppp_maladie_proche_aidant_id=None, access_token=None, **kw
    ):
        try:
            ceppp_maladie_proche_aidant_sudo = self._document_check_access(
                "ceppp.maladie_proche_aidant",
                ceppp_maladie_proche_aidant_id,
                access_token,
            )
        except (AccessError, MissingError):
            return request.redirect("/my")

        values = self._ceppp_maladie_proche_aidant_get_page_view_values(
            ceppp_maladie_proche_aidant_sudo, access_token, **kw
        )
        return request.render(
            "ceppp_patient_partenaire.portal_my_ceppp_maladie_proche_aidant",
            values,
        )

    # ------------------------------------------------------------
    # My Ceppp Mode_Communication_Privilegie
    # ------------------------------------------------------------
    def _ceppp_mode_communication_privilegie_get_page_view_values(
        self, ceppp_mode_communication_privilegie, access_token, **kwargs
    ):
        values = {
            "page_name": "ceppp_mode_communication_privilegie",
            "ceppp_mode_communication_privilegie": ceppp_mode_communication_privilegie,
            "user": request.env.user,
        }
        return self._get_page_view_values(
            ceppp_mode_communication_privilegie,
            access_token,
            values,
            "my_ceppp_mode_communication_privilegies_history",
            False,
            **kwargs,
        )

    @http.route(
        [
            "/my/ceppp_mode_communication_privilegies",
            "/my/ceppp_mode_communication_privilegies/page/<int:page>",
        ],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_ceppp_mode_communication_privilegies(
        self,
        page=1,
        date_begin=None,
        date_end=None,
        sortby=None,
        filterby=None,
        search=None,
        search_in="content",
        **kw,
    ):
        values = self._prepare_portal_layout_values()
        CepppModeCommunicationPrivilegie = request.env[
            "ceppp.mode_communication_privilegie"
        ]
        domain = []

        searchbar_sortings = {
            "date": {"label": _("Newest"), "order": "create_date desc"},
            "name": {"label": _("Name"), "order": "name"},
        }
        searchbar_filters = {
            "all": {"label": _("All"), "domain": []},
        }
        searchbar_inputs = {}
        searchbar_groupby = {}

        # default sort by value
        if not sortby:
            sortby = "date"
        order = searchbar_sortings[sortby]["order"]
        # default filter by value
        if not filterby:
            filterby = "all"
        domain = searchbar_filters[filterby]["domain"]

        # search
        if search and search_in:
            search_domain = []
            domain += search_domain
        # archive groups - Default Group By 'create_date'
        archive_groups = self._get_archive_groups(
            "ceppp.mode_communication_privilegie", domain
        )
        if date_begin and date_end:
            domain += [
                ("create_date", ">", date_begin),
                ("create_date", "<=", date_end),
            ]
        # ceppp_mode_communication_privilegies count
        ceppp_mode_communication_privilegie_count = (
            CepppModeCommunicationPrivilegie.search_count(domain)
        )
        # pager
        pager = portal_pager(
            url="/my/ceppp_mode_communication_privilegies",
            url_args={
                "date_begin": date_begin,
                "date_end": date_end,
                "sortby": sortby,
                "filterby": filterby,
                "search_in": search_in,
                "search": search,
            },
            total=ceppp_mode_communication_privilegie_count,
            page=page,
            step=self._items_per_page,
        )

        # content according to pager and archive selected
        ceppp_mode_communication_privilegies = (
            CepppModeCommunicationPrivilegie.search(
                domain,
                order=order,
                limit=self._items_per_page,
                offset=pager["offset"],
            )
        )
        request.session[
            "my_ceppp_mode_communication_privilegies_history"
        ] = ceppp_mode_communication_privilegies.ids[:100]

        values.update(
            {
                "date": date_begin,
                "date_end": date_end,
                "ceppp_mode_communication_privilegies": ceppp_mode_communication_privilegies,
                "page_name": "ceppp_mode_communication_privilegie",
                "archive_groups": archive_groups,
                "default_url": "/my/ceppp_mode_communication_privilegies",
                "pager": pager,
                "searchbar_sortings": searchbar_sortings,
                "searchbar_groupby": searchbar_groupby,
                "searchbar_inputs": searchbar_inputs,
                "search_in": search_in,
                "searchbar_filters": OrderedDict(
                    sorted(searchbar_filters.items())
                ),
                "sortby": sortby,
                "filterby": filterby,
            }
        )
        return request.render(
            "ceppp_patient_partenaire.portal_my_ceppp_mode_communication_privilegies",
            values,
        )

    @http.route(
        [
            "/my/ceppp_mode_communication_privilegie/<int:ceppp_mode_communication_privilegie_id>"
        ],
        type="http",
        auth="public",
        website=True,
    )
    def portal_my_ceppp_mode_communication_privilegie(
        self,
        ceppp_mode_communication_privilegie_id=None,
        access_token=None,
        **kw,
    ):
        try:
            ceppp_mode_communication_privilegie_sudo = (
                self._document_check_access(
                    "ceppp.mode_communication_privilegie",
                    ceppp_mode_communication_privilegie_id,
                    access_token,
                )
            )
        except (AccessError, MissingError):
            return request.redirect("/my")

        values = (
            self._ceppp_mode_communication_privilegie_get_page_view_values(
                ceppp_mode_communication_privilegie_sudo, access_token, **kw
            )
        )
        return request.render(
            "ceppp_patient_partenaire.portal_my_ceppp_mode_communication_privilegie",
            values,
        )

    # ------------------------------------------------------------
    # My Ceppp Occupation
    # ------------------------------------------------------------
    def _ceppp_occupation_get_page_view_values(
        self, ceppp_occupation, access_token, **kwargs
    ):
        values = {
            "page_name": "ceppp_occupation",
            "ceppp_occupation": ceppp_occupation,
            "user": request.env.user,
        }
        return self._get_page_view_values(
            ceppp_occupation,
            access_token,
            values,
            "my_ceppp_occupations_history",
            False,
            **kwargs,
        )

    @http.route(
        ["/my/ceppp_occupations", "/my/ceppp_occupations/page/<int:page>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_ceppp_occupations(
        self,
        page=1,
        date_begin=None,
        date_end=None,
        sortby=None,
        filterby=None,
        search=None,
        search_in="content",
        **kw,
    ):
        values = self._prepare_portal_layout_values()
        CepppOccupation = request.env["ceppp.occupation"]
        domain = []

        searchbar_sortings = {
            "date": {"label": _("Newest"), "order": "create_date desc"},
            "name": {"label": _("Name"), "order": "name"},
        }
        searchbar_filters = {
            "all": {"label": _("All"), "domain": []},
        }
        searchbar_inputs = {}
        searchbar_groupby = {}

        # default sort by value
        if not sortby:
            sortby = "date"
        order = searchbar_sortings[sortby]["order"]
        # default filter by value
        if not filterby:
            filterby = "all"
        domain = searchbar_filters[filterby]["domain"]

        # search
        if search and search_in:
            search_domain = []
            domain += search_domain
        # archive groups - Default Group By 'create_date'
        archive_groups = self._get_archive_groups("ceppp.occupation", domain)
        if date_begin and date_end:
            domain += [
                ("create_date", ">", date_begin),
                ("create_date", "<=", date_end),
            ]
        # ceppp_occupations count
        ceppp_occupation_count = CepppOccupation.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/ceppp_occupations",
            url_args={
                "date_begin": date_begin,
                "date_end": date_end,
                "sortby": sortby,
                "filterby": filterby,
                "search_in": search_in,
                "search": search,
            },
            total=ceppp_occupation_count,
            page=page,
            step=self._items_per_page,
        )

        # content according to pager and archive selected
        ceppp_occupations = CepppOccupation.search(
            domain,
            order=order,
            limit=self._items_per_page,
            offset=pager["offset"],
        )
        request.session[
            "my_ceppp_occupations_history"
        ] = ceppp_occupations.ids[:100]

        values.update(
            {
                "date": date_begin,
                "date_end": date_end,
                "ceppp_occupations": ceppp_occupations,
                "page_name": "ceppp_occupation",
                "archive_groups": archive_groups,
                "default_url": "/my/ceppp_occupations",
                "pager": pager,
                "searchbar_sortings": searchbar_sortings,
                "searchbar_groupby": searchbar_groupby,
                "searchbar_inputs": searchbar_inputs,
                "search_in": search_in,
                "searchbar_filters": OrderedDict(
                    sorted(searchbar_filters.items())
                ),
                "sortby": sortby,
                "filterby": filterby,
            }
        )
        return request.render(
            "ceppp_patient_partenaire.portal_my_ceppp_occupations", values
        )

    @http.route(
        ["/my/ceppp_occupation/<int:ceppp_occupation_id>"],
        type="http",
        auth="public",
        website=True,
    )
    def portal_my_ceppp_occupation(
        self, ceppp_occupation_id=None, access_token=None, **kw
    ):
        try:
            ceppp_occupation_sudo = self._document_check_access(
                "ceppp.occupation", ceppp_occupation_id, access_token
            )
        except (AccessError, MissingError):
            return request.redirect("/my")

        values = self._ceppp_occupation_get_page_view_values(
            ceppp_occupation_sudo, access_token, **kw
        )
        return request.render(
            "ceppp_patient_partenaire.portal_my_ceppp_occupation", values
        )

    # ------------------------------------------------------------
    # My Ceppp Patient
    # ------------------------------------------------------------
    def _ceppp_patient_get_page_view_values(
        self, ceppp_patient, access_token, **kwargs
    ):
        values = {
            "page_name": "ceppp_patient",
            "ceppp_patient": ceppp_patient,
            "user": request.env.user,
        }
        return self._get_page_view_values(
            ceppp_patient,
            access_token,
            values,
            "my_ceppp_patients_history",
            False,
            **kwargs,
        )

    @http.route(
        ["/my/ceppp_patients", "/my/ceppp_patients/page/<int:page>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_ceppp_patients(
        self,
        page=1,
        date_begin=None,
        date_end=None,
        sortby=None,
        filterby=None,
        search=None,
        search_in="content",
        **kw,
    ):
        values = self._prepare_portal_layout_values()
        CepppPatient = request.env["ceppp.patient"]
        domain = []

        searchbar_sortings = {
            "date": {"label": _("Newest"), "order": "create_date desc"},
            "name": {"label": _("Name"), "order": "name"},
        }
        searchbar_filters = {
            "all": {"label": _("All"), "domain": []},
        }
        searchbar_inputs = {}
        searchbar_groupby = {}

        # default sort by value
        if not sortby:
            sortby = "date"
        order = searchbar_sortings[sortby]["order"]
        # default filter by value
        if not filterby:
            filterby = "all"
        domain = searchbar_filters[filterby]["domain"]

        # search
        if search and search_in:
            search_domain = []
            domain += search_domain
        # archive groups - Default Group By 'create_date'
        archive_groups = self._get_archive_groups("ceppp.patient", domain)
        if date_begin and date_end:
            domain += [
                ("create_date", ">", date_begin),
                ("create_date", "<=", date_end),
            ]
        # ceppp_patients count
        ceppp_patient_count = CepppPatient.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/ceppp_patients",
            url_args={
                "date_begin": date_begin,
                "date_end": date_end,
                "sortby": sortby,
                "filterby": filterby,
                "search_in": search_in,
                "search": search,
            },
            total=ceppp_patient_count,
            page=page,
            step=self._items_per_page,
        )

        # content according to pager and archive selected
        ceppp_patients = CepppPatient.search(
            domain,
            order=order,
            limit=self._items_per_page,
            offset=pager["offset"],
        )
        request.session["my_ceppp_patients_history"] = ceppp_patients.ids[:100]

        values.update(
            {
                "date": date_begin,
                "date_end": date_end,
                "ceppp_patients": ceppp_patients,
                "page_name": "ceppp_patient",
                "archive_groups": archive_groups,
                "default_url": "/my/ceppp_patients",
                "pager": pager,
                "searchbar_sortings": searchbar_sortings,
                "searchbar_groupby": searchbar_groupby,
                "searchbar_inputs": searchbar_inputs,
                "search_in": search_in,
                "searchbar_filters": OrderedDict(
                    sorted(searchbar_filters.items())
                ),
                "sortby": sortby,
                "filterby": filterby,
            }
        )
        return request.render(
            "ceppp_patient_partenaire.portal_my_ceppp_patients", values
        )

    @http.route(
        ["/my/ceppp_patient/<int:ceppp_patient_id>"],
        type="http",
        auth="public",
        website=True,
    )
    def portal_my_ceppp_patient(
        self, ceppp_patient_id=None, access_token=None, **kw
    ):
        try:
            ceppp_patient_sudo = self._document_check_access(
                "ceppp.patient", ceppp_patient_id, access_token
            )
        except (AccessError, MissingError):
            return request.redirect("/my")

        values = self._ceppp_patient_get_page_view_values(
            ceppp_patient_sudo, access_token, **kw
        )
        return request.render(
            "ceppp_patient_partenaire.portal_my_ceppp_patient", values
        )

    # ------------------------------------------------------------
    # My Ceppp Recruteur
    # ------------------------------------------------------------
    def _ceppp_recruteur_get_page_view_values(
        self, ceppp_recruteur, access_token, **kwargs
    ):
        values = {
            "page_name": "ceppp_recruteur",
            "ceppp_recruteur": ceppp_recruteur,
            "user": request.env.user,
        }
        return self._get_page_view_values(
            ceppp_recruteur,
            access_token,
            values,
            "my_ceppp_recruteurs_history",
            False,
            **kwargs,
        )

    @http.route(
        ["/my/ceppp_recruteurs", "/my/ceppp_recruteurs/page/<int:page>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_ceppp_recruteurs(
        self,
        page=1,
        date_begin=None,
        date_end=None,
        sortby=None,
        filterby=None,
        search=None,
        search_in="content",
        **kw,
    ):
        values = self._prepare_portal_layout_values()
        CepppRecruteur = request.env["ceppp.recruteur"]
        domain = []

        searchbar_sortings = {
            "date": {"label": _("Newest"), "order": "create_date desc"},
            "name": {"label": _("Name"), "order": "name"},
        }
        searchbar_filters = {
            "all": {"label": _("All"), "domain": []},
        }
        searchbar_inputs = {}
        searchbar_groupby = {}

        # default sort by value
        if not sortby:
            sortby = "date"
        order = searchbar_sortings[sortby]["order"]
        # default filter by value
        if not filterby:
            filterby = "all"
        domain = searchbar_filters[filterby]["domain"]

        # search
        if search and search_in:
            search_domain = []
            domain += search_domain
        # archive groups - Default Group By 'create_date'
        archive_groups = self._get_archive_groups("ceppp.recruteur", domain)
        if date_begin and date_end:
            domain += [
                ("create_date", ">", date_begin),
                ("create_date", "<=", date_end),
            ]
        # ceppp_recruteurs count
        ceppp_recruteur_count = CepppRecruteur.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/ceppp_recruteurs",
            url_args={
                "date_begin": date_begin,
                "date_end": date_end,
                "sortby": sortby,
                "filterby": filterby,
                "search_in": search_in,
                "search": search,
            },
            total=ceppp_recruteur_count,
            page=page,
            step=self._items_per_page,
        )

        # content according to pager and archive selected
        ceppp_recruteurs = CepppRecruteur.search(
            domain,
            order=order,
            limit=self._items_per_page,
            offset=pager["offset"],
        )
        request.session["my_ceppp_recruteurs_history"] = ceppp_recruteurs.ids[
            :100
        ]

        values.update(
            {
                "date": date_begin,
                "date_end": date_end,
                "ceppp_recruteurs": ceppp_recruteurs,
                "page_name": "ceppp_recruteur",
                "archive_groups": archive_groups,
                "default_url": "/my/ceppp_recruteurs",
                "pager": pager,
                "searchbar_sortings": searchbar_sortings,
                "searchbar_groupby": searchbar_groupby,
                "searchbar_inputs": searchbar_inputs,
                "search_in": search_in,
                "searchbar_filters": OrderedDict(
                    sorted(searchbar_filters.items())
                ),
                "sortby": sortby,
                "filterby": filterby,
            }
        )
        return request.render(
            "ceppp_patient_partenaire.portal_my_ceppp_recruteurs", values
        )

    @http.route(
        ["/my/ceppp_recruteur/<int:ceppp_recruteur_id>"],
        type="http",
        auth="public",
        website=True,
    )
    def portal_my_ceppp_recruteur(
        self, ceppp_recruteur_id=None, access_token=None, **kw
    ):
        try:
            ceppp_recruteur_sudo = self._document_check_access(
                "ceppp.recruteur", ceppp_recruteur_id, access_token
            )
        except (AccessError, MissingError):
            return request.redirect("/my")

        values = self._ceppp_recruteur_get_page_view_values(
            ceppp_recruteur_sudo, access_token, **kw
        )
        return request.render(
            "ceppp_patient_partenaire.portal_my_ceppp_recruteur", values
        )

    # ------------------------------------------------------------
    # My Ceppp Relation_Proche
    # ------------------------------------------------------------
    def _ceppp_relation_proche_get_page_view_values(
        self, ceppp_relation_proche, access_token, **kwargs
    ):
        values = {
            "page_name": "ceppp_relation_proche",
            "ceppp_relation_proche": ceppp_relation_proche,
            "user": request.env.user,
        }
        return self._get_page_view_values(
            ceppp_relation_proche,
            access_token,
            values,
            "my_ceppp_relation_proches_history",
            False,
            **kwargs,
        )

    @http.route(
        [
            "/my/ceppp_relation_proches",
            "/my/ceppp_relation_proches/page/<int:page>",
        ],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_ceppp_relation_proches(
        self,
        page=1,
        date_begin=None,
        date_end=None,
        sortby=None,
        filterby=None,
        search=None,
        search_in="content",
        **kw,
    ):
        values = self._prepare_portal_layout_values()
        CepppRelationProche = request.env["ceppp.relation_proche"]
        domain = []

        searchbar_sortings = {
            "date": {"label": _("Newest"), "order": "create_date desc"},
            "name": {"label": _("Name"), "order": "name"},
        }
        searchbar_filters = {
            "all": {"label": _("All"), "domain": []},
        }
        searchbar_inputs = {}
        searchbar_groupby = {}

        # default sort by value
        if not sortby:
            sortby = "date"
        order = searchbar_sortings[sortby]["order"]
        # default filter by value
        if not filterby:
            filterby = "all"
        domain = searchbar_filters[filterby]["domain"]

        # search
        if search and search_in:
            search_domain = []
            domain += search_domain
        # archive groups - Default Group By 'create_date'
        archive_groups = self._get_archive_groups(
            "ceppp.relation_proche", domain
        )
        if date_begin and date_end:
            domain += [
                ("create_date", ">", date_begin),
                ("create_date", "<=", date_end),
            ]
        # ceppp_relation_proches count
        ceppp_relation_proche_count = CepppRelationProche.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/ceppp_relation_proches",
            url_args={
                "date_begin": date_begin,
                "date_end": date_end,
                "sortby": sortby,
                "filterby": filterby,
                "search_in": search_in,
                "search": search,
            },
            total=ceppp_relation_proche_count,
            page=page,
            step=self._items_per_page,
        )

        # content according to pager and archive selected
        ceppp_relation_proches = CepppRelationProche.search(
            domain,
            order=order,
            limit=self._items_per_page,
            offset=pager["offset"],
        )
        request.session[
            "my_ceppp_relation_proches_history"
        ] = ceppp_relation_proches.ids[:100]

        values.update(
            {
                "date": date_begin,
                "date_end": date_end,
                "ceppp_relation_proches": ceppp_relation_proches,
                "page_name": "ceppp_relation_proche",
                "archive_groups": archive_groups,
                "default_url": "/my/ceppp_relation_proches",
                "pager": pager,
                "searchbar_sortings": searchbar_sortings,
                "searchbar_groupby": searchbar_groupby,
                "searchbar_inputs": searchbar_inputs,
                "search_in": search_in,
                "searchbar_filters": OrderedDict(
                    sorted(searchbar_filters.items())
                ),
                "sortby": sortby,
                "filterby": filterby,
            }
        )
        return request.render(
            "ceppp_patient_partenaire.portal_my_ceppp_relation_proches", values
        )

    @http.route(
        ["/my/ceppp_relation_proche/<int:ceppp_relation_proche_id>"],
        type="http",
        auth="public",
        website=True,
    )
    def portal_my_ceppp_relation_proche(
        self, ceppp_relation_proche_id=None, access_token=None, **kw
    ):
        try:
            ceppp_relation_proche_sudo = self._document_check_access(
                "ceppp.relation_proche", ceppp_relation_proche_id, access_token
            )
        except (AccessError, MissingError):
            return request.redirect("/my")

        values = self._ceppp_relation_proche_get_page_view_values(
            ceppp_relation_proche_sudo, access_token, **kw
        )
        return request.render(
            "ceppp_patient_partenaire.portal_my_ceppp_relation_proche", values
        )
