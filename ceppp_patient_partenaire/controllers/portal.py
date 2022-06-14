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
        values["ceppp_formation_count"] = request.env[
            "ceppp.formation"
        ].search_count([])
        values["ceppp_implication_count"] = request.env[
            "ceppp.implication"
        ].search_count([])
        values["ceppp_maladie_count"] = request.env[
            "ceppp.maladie"
        ].search_count([])
        values["ceppp_maladie_proche_aidant_count"] = request.env[
            "ceppp.maladie_proche_aidant"
        ].search_count([])
        return values

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
