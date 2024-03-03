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
    def __init__(self):
        # super().__init__()
        self.ORIGIN_OPTIONAL_BILLING_FIELDS = self.OPTIONAL_BILLING_FIELDS[:]
        self.RECRUTEUR_FIELDS = [
            "langue_parle_ecrit",
            "langue_parle_ecrit_autre",
            "occupation",
            "occupation_autre",
        ]
        self.RECRUTEUR_FIELDS_M2M = ["langue_parle_ecrit", "occupation"]
        self.OPTIONAL_BILLING_FIELDS.extend(self.RECRUTEUR_FIELDS)

    def _prepare_portal_layout_values(self):
        values = super(
            CepppPatientPartenaireController, self
        )._prepare_portal_layout_values()
        pp_id = request.env.user.partner_id.patient_partner_ids
        if pp_id:
            values["ceppp_formation_count"] = request.env[
                "ceppp.formation"
            ].search_count(
                [
                    (
                        "recruteur_id",
                        "in",
                        [pp_id.id],
                    )
                ]
            )
            values["ceppp_implication_count"] = request.env[
                "ceppp.implication"
            ].search_count(
                [
                    (
                        "recruteur_id",
                        "in",
                        [pp_id.id],
                    )
                ]
            )
            values["ceppp_maladie_count"] = request.env[
                "ceppp.maladie"
            ].search_count([])
            values["ceppp_maladie_personne_affectee_count"] = request.env[
                "ceppp.maladie_personne_affectee"
            ].search_count(
                [
                    (
                        "recruteur_id",
                        "in",
                        [pp_id.id],
                    )
                ]
            )

            values["ceppp_recruteur"] = pp_id
        else:
            values["ceppp_formation_count"] = 0
            values["ceppp_implication_count"] = 0
            values["ceppp_maladie_count"] = 0
            values["ceppp_maladie_personne_affectee_count"] = 0
            values["ceppp_recruteur"] = None
        values["is_patient"] = (
            request.env.user.partner_id.ceppp_entity == "patient"
        )
        values["all_disponibilite"] = request.env[
            "ceppp.disponibilite"
        ].search([])
        values["all_maladie"] = request.env["ceppp.maladie"].search([])
        values["all_chapitre_maladie"] = request.env[
            "ceppp.chapitre_maladie"
        ].search([])
        values["all_mode_communication_privilegie"] = request.env[
            "ceppp.mode_communication_privilegie"
        ].search([])
        return values

    # ------------------------------------------------------------
    # My Ceppp Formation
    # ------------------------------------------------------------
    def _ceppp_formation_get_page_view_values(
        self, ceppp_formation, access_token, **kwargs
    ):
        formation_titre = http.request.env["ceppp.formation_titre"].search([])
        values = {
            "page_name": "ceppp_formation",
            "ceppp_formation": ceppp_formation,
            "user": request.env.user,
            "ceppp_formation_titre": formation_titre,
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
        domain += [
            (
                "recruteur_id",
                "in",
                [request.env.user.partner_id.patient_partner_ids.id],
            )
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
    # My Ceppp Implication
    # ------------------------------------------------------------
    def _ceppp_implication_get_page_view_values(
        self, ceppp_implication, access_token, **kwargs
    ):
        domaine = http.request.env["ceppp.implication_domaine"].search([])
        role = http.request.env["ceppp.implication_role"].search([])
        values = {
            "page_name": "ceppp_implication",
            "ceppp_implication": ceppp_implication,
            "user": request.env.user,
            "ceppp_implication_domaine": domaine,
            "ceppp_implication_role": role,
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
        # Restrict access data
        domain += [
            (
                "recruteur_id",
                "in",
                [request.env.user.partner_id.patient_partner_ids.id],
            )
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
        domain += [
            (
                "recruteur_id",
                "in",
                [request.env.user.partner_id.patient_partner_ids.id],
            )
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
    # My Ceppp Maladie_Personne_Affectee
    # ------------------------------------------------------------
    def _ceppp_maladie_personne_affectee_get_page_view_values(
        self, ceppp_maladie_personne_affectee, access_token, **kwargs
    ):
        relation = http.request.env["ceppp.relation_proche"].search([])
        maladie_autocomplete = "; ".join(
            [a.nom for a in ceppp_maladie_personne_affectee.maladie]
        )
        if maladie_autocomplete:
            maladie_autocomplete += "; "
        if ceppp_maladie_personne_affectee.autre_maladie:
            maladie_autocomplete += (
                ceppp_maladie_personne_affectee.autre_maladie
            )
        values = {
            "page_name": "ceppp_maladie_personne_affectee",
            "ceppp_maladie_personne_affectee": ceppp_maladie_personne_affectee,
            "maladie_autocomplete": maladie_autocomplete,
            "user": request.env.user,
            "ceppp_maladie_personne_affectee_relation": relation,
        }
        return self._get_page_view_values(
            ceppp_maladie_personne_affectee,
            access_token,
            values,
            "my_ceppp_maladie_personne_affectees_history",
            False,
            **kwargs,
        )

    @http.route(
        [
            "/my/ceppp_maladie_personne_affectees",
            "/my/ceppp_maladie_personne_affectees/page/<int:page>",
        ],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_ceppp_maladie_personne_affectees(
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
        CepppMaladiePersonneAffectee = request.env[
            "ceppp.maladie_personne_affectee"
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
            "ceppp.maladie_personne_affectee", domain
        )
        if date_begin and date_end:
            domain += [
                ("create_date", ">", date_begin),
                ("create_date", "<=", date_end),
            ]
        # ceppp_maladie_personne_affectees count
        ceppp_maladie_personne_affectee_count = (
            CepppMaladiePersonneAffectee.search_count(domain)
        )
        domain += [
            (
                "recruteur_id",
                "in",
                [request.env.user.partner_id.patient_partner_ids.id],
            )
        ]
        # pager
        pager = portal_pager(
            url="/my/ceppp_maladie_personne_affectees",
            url_args={
                "date_begin": date_begin,
                "date_end": date_end,
                "sortby": sortby,
                "filterby": filterby,
                "search_in": search_in,
                "search": search,
            },
            total=ceppp_maladie_personne_affectee_count,
            page=page,
            step=self._items_per_page,
        )

        # content according to pager and archive selected
        ceppp_maladie_personne_affectees = CepppMaladiePersonneAffectee.search(
            domain,
            order=order,
            limit=self._items_per_page,
            offset=pager["offset"],
        )
        request.session[
            "my_ceppp_maladie_personne_affectees_history"
        ] = ceppp_maladie_personne_affectees.ids[:100]

        domain_is_me = domain + [
            ("is_me", "=", True),
            ("id", "in", ceppp_maladie_personne_affectees.ids),
        ]
        ceppp_maladie_personne_affectees_is_me = (
            ceppp_maladie_personne_affectees.search(domain_is_me, order=order)
        )
        domain_is_me = domain + [
            ("is_proche_aidant", "=", True),
            ("id", "in", ceppp_maladie_personne_affectees.ids),
        ]
        ceppp_maladie_personne_affectees_is_proche_aidant = (
            ceppp_maladie_personne_affectees.search(domain_is_me, order=order)
        )

        values.update(
            {
                "date": date_begin,
                "date_end": date_end,
                "ceppp_maladie_personne_affectees": ceppp_maladie_personne_affectees,
                "ceppp_maladie_personne_affectees_is_me": ceppp_maladie_personne_affectees_is_me,
                "ceppp_maladie_personne_affectees_is_proche_aidant": ceppp_maladie_personne_affectees_is_proche_aidant,
                "count_is_me": len(ceppp_maladie_personne_affectees_is_me),
                "count_is_proche_aidant": len(
                    ceppp_maladie_personne_affectees_is_proche_aidant
                ),
                "page_name": "ceppp_maladie_personne_affectee",
                "archive_groups": archive_groups,
                "default_url": "/my/ceppp_maladie_personne_affectees",
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
            "ceppp_patient_partenaire.portal_my_ceppp_maladie_personne_affectees",
            values,
        )

    @http.route(
        [
            "/my/ceppp_maladie_personne_affectee/<int:ceppp_maladie_personne_affectee_id>"
        ],
        type="http",
        auth="public",
        website=True,
    )
    def portal_my_ceppp_maladie_personne_affectee(
        self, ceppp_maladie_personne_affectee_id=None, access_token=None, **kw
    ):
        try:
            ceppp_maladie_personne_affectee_sudo = self._document_check_access(
                "ceppp.maladie_personne_affectee",
                ceppp_maladie_personne_affectee_id,
                access_token,
            )
        except (AccessError, MissingError):
            return request.redirect("/my")

        values = self._ceppp_maladie_personne_affectee_get_page_view_values(
            ceppp_maladie_personne_affectee_sudo, access_token, **kw
        )
        return request.render(
            "ceppp_patient_partenaire.portal_my_ceppp_maladie_personne_affectee",
            values,
        )

    @http.route(["/my/account"], type="http", auth="user", website=True)
    def account(self, redirect=None, **post):
        # Overwrite portal/controllers/portal.py
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        values.update(
            {
                "error": {},
                "error_message": [],
            }
        )

        if post and request.httprequest.method == "POST":
            error, error_message = self.details_form_validate(post)
            values.update({"error": error, "error_message": error_message})
            values.update(post)
            if not error:
                values = {
                    key: post[key] for key in self.MANDATORY_BILLING_FIELDS
                }
                # Change OPTIONAL_BILLING_FIELDS to ORIGIN_OPTIONAL_BILLING_FIELDS
                values.update(
                    {
                        key: post[key]
                        for key in self.ORIGIN_OPTIONAL_BILLING_FIELDS
                        if key in post
                    }
                )
                values.update({"zip": values.pop("zipcode", "")})
                partner.sudo().write(values)
                # ADD below
                recruteur_id = partner.patient_partner_ids
                if recruteur_id:
                    values_recruteur = {}
                    for key in self.RECRUTEUR_FIELDS:
                        if key not in post:
                            continue
                        if key in self.RECRUTEUR_FIELDS_M2M:
                            v = [
                                (
                                    6,
                                    0,
                                    [
                                        int(a)
                                        for a in request.httprequest.form.getlist(
                                            key
                                        )
                                    ],
                                )
                            ]
                        else:
                            v = post[key]
                        values_recruteur[key] = v
                    recruteur_id.sudo().write(values_recruteur)
                # End ADD
                if redirect:
                    return request.redirect(redirect)
                return request.redirect("/my/home")

        countries = request.env["res.country"].sudo().search([])
        states = request.env["res.country.state"].sudo().search([])

        all_langue_parle_ecrit = request.env["ceppp.langue"].search([])
        all_occupation = request.env["ceppp.occupation"].search([])
        recruteur_id = request.env.user.partner_id.patient_partner_ids

        values.update(
            {
                "partner": partner,
                "countries": countries,
                "states": states,
                "has_check_vat": hasattr(
                    request.env["res.partner"], "check_vat"
                ),
                "redirect": redirect,
                "page_name": "my_details",
                "ceppp_recruteur": recruteur_id,
                "all_langue_parle_ecrit": all_langue_parle_ecrit,
                "all_occupation": all_occupation,
            }
        )

        response = request.render("portal.portal_my_details", values)
        response.headers["X-Frame-Options"] = "DENY"
        return response
