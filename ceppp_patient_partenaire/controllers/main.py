import base64
import logging

import werkzeug

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class CepppPatientPartenaireController(http.Controller):
    @http.route("/new/ceppp_formation", type="http", auth="user", website=True)
    def create_new_ceppp_formation(self, **kw):
        name = http.request.env.user.name
        default_date = (
            http.request.env["ceppp.formation"]
            .default_get(["date"])
            .get("date")
        )
        default_organisation = (
            http.request.env["ceppp.formation"]
            .default_get(["organisation"])
            .get("organisation")
        )
        recruteur_id = http.request.env["ceppp.recruteur"].search(
            [("active", "=", True)]
        )
        default_recruteur_id = (
            http.request.env["ceppp.formation"]
            .default_get(["recruteur_id"])
            .get("recruteur_id")
        )
        titre_formation = http.request.env["ceppp.formation_titre"].search([])
        lst_default_titre_formation = (
            http.request.env["ceppp.formation"]
            .default_get(["titre_formation"])
            .get("titre_formation")
        )
        if lst_default_titre_formation:
            default_titre_formation = lst_default_titre_formation[0][2]
        else:
            default_titre_formation = []
        default_titre_formation_autre = (
            http.request.env["ceppp.formation"]
            .default_get(["titre_formation_autre"])
            .get("titre_formation_autre")
        )
        default_titre_formation_is_autre = (
            http.request.env["ceppp.formation"]
            .default_get(["titre_formation_is_autre"])
            .get("titre_formation_is_autre")
        )
        return http.request.render(
            "ceppp_patient_partenaire.portal_create_ceppp_formation",
            {
                "name": name,
                "recruteur_id": recruteur_id,
                "titre_formation": titre_formation,
                "page_name": "create_ceppp_formation",
                "default_date": default_date,
                "default_organisation": default_organisation,
                "default_recruteur_id": default_recruteur_id,
                "default_titre_formation": default_titre_formation,
                "default_titre_formation_autre": default_titre_formation_autre,
                "default_titre_formation_is_autre": default_titre_formation_is_autre,
            },
        )

    @http.route(
        "/submitted/ceppp_formation",
        type="http",
        auth="user",
        website=True,
        csrf=True,
    )
    def submit_ceppp_formation(self, **kw):
        vals = {}

        # if kw.get("name"):
        #     vals["name"] = kw.get("name")

        if kw.get("date"):
            vals["date"] = kw.get("date")

        if kw.get("organisation"):
            vals["organisation"] = kw.get("organisation")

        if kw.get("recruteur_id") and kw.get("recruteur_id").isdigit():
            vals["recruteur_id"] = int(kw.get("recruteur_id"))

        if kw.get("titre_formation"):
            lst_value_titre_formation = [
                (4, int(a))
                for a in request.httprequest.form.getlist("titre_formation")
            ]
            vals["titre_formation"] = lst_value_titre_formation

        if kw.get("titre_formation_autre"):
            vals["titre_formation_autre"] = kw.get("titre_formation_autre")

        default_titre_formation_is_autre = (
            http.request.env["ceppp.formation"]
            .default_get(["titre_formation_is_autre"])
            .get("titre_formation_is_autre")
        )
        if kw.get("titre_formation_is_autre"):
            vals["titre_formation_is_autre"] = (
                kw.get("titre_formation_is_autre") == "True"
            )
        elif default_titre_formation_is_autre:
            vals["titre_formation_is_autre"] = False

        new_ceppp_formation = (
            request.env["ceppp.formation"].sudo().create(vals)
        )
        return werkzeug.utils.redirect(
            f"/my/ceppp_formation/{new_ceppp_formation.id}"
        )

    @http.route(
        "/new/ceppp_implication", type="http", auth="user", website=True
    )
    def create_new_ceppp_implication(self, **kw):
        name = http.request.env.user.name
        default_description = (
            http.request.env["ceppp.implication"]
            .default_get(["description"])
            .get("description")
        )
        domaine = http.request.env["ceppp.implication_domaine"].search([])
        lst_default_domaine = (
            http.request.env["ceppp.implication"]
            .default_get(["domaine"])
            .get("domaine")
        )
        if lst_default_domaine:
            default_domaine = lst_default_domaine[0][2]
        else:
            default_domaine = []
        default_domaine_autre = (
            http.request.env["ceppp.implication"]
            .default_get(["domaine_autre"])
            .get("domaine_autre")
        )
        default_domaine_is_autre = (
            http.request.env["ceppp.implication"]
            .default_get(["domaine_is_autre"])
            .get("domaine_is_autre")
        )
        default_echeance_debut = (
            http.request.env["ceppp.implication"]
            .default_get(["echeance_debut"])
            .get("echeance_debut")
        )
        default_echeance_fin = (
            http.request.env["ceppp.implication"]
            .default_get(["echeance_fin"])
            .get("echeance_fin")
        )
        default_nom_equipe = (
            http.request.env["ceppp.implication"]
            .default_get(["nom_equipe"])
            .get("nom_equipe")
        )
        recruteur_id = http.request.env["ceppp.recruteur"].search(
            [("active", "=", True)]
        )
        default_recruteur_id = (
            http.request.env["ceppp.implication"]
            .default_get(["recruteur_id"])
            .get("recruteur_id")
        )
        role = http.request.env["ceppp.implication_role"].search([])
        lst_default_role = (
            http.request.env["ceppp.implication"]
            .default_get(["role"])
            .get("role")
        )
        if lst_default_role:
            default_role = lst_default_role[0][2]
        else:
            default_role = []
        default_role_autre = (
            http.request.env["ceppp.implication"]
            .default_get(["role_autre"])
            .get("role_autre")
        )
        default_role_is_autre = (
            http.request.env["ceppp.implication"]
            .default_get(["role_is_autre"])
            .get("role_is_autre")
        )
        default_titre = (
            http.request.env["ceppp.implication"]
            .default_get(["titre"])
            .get("titre")
        )
        return http.request.render(
            "ceppp_patient_partenaire.portal_create_ceppp_implication",
            {
                "name": name,
                "domaine": domaine,
                "recruteur_id": recruteur_id,
                "role": role,
                "page_name": "create_ceppp_implication",
                "default_description": default_description,
                "default_domaine": default_domaine,
                "default_domaine_autre": default_domaine_autre,
                "default_domaine_is_autre": default_domaine_is_autre,
                "default_echeance_debut": default_echeance_debut,
                "default_echeance_fin": default_echeance_fin,
                "default_nom_equipe": default_nom_equipe,
                "default_recruteur_id": default_recruteur_id,
                "default_role": default_role,
                "default_role_autre": default_role_autre,
                "default_role_is_autre": default_role_is_autre,
                "default_titre": default_titre,
            },
        )

    @http.route(
        "/submitted/ceppp_implication",
        type="http",
        auth="user",
        website=True,
        csrf=True,
    )
    def submit_ceppp_implication(self, **kw):
        vals = {}

        # if kw.get("name"):
        #     vals["name"] = kw.get("name")

        if kw.get("description"):
            vals["description"] = kw.get("description")

        if kw.get("domaine"):
            lst_value_domaine = [
                (4, int(a))
                for a in request.httprequest.form.getlist("domaine")
            ]
            vals["domaine"] = lst_value_domaine

        if kw.get("domaine_autre"):
            vals["domaine_autre"] = kw.get("domaine_autre")

        default_domaine_is_autre = (
            http.request.env["ceppp.implication"]
            .default_get(["domaine_is_autre"])
            .get("domaine_is_autre")
        )
        if kw.get("domaine_is_autre"):
            vals["domaine_is_autre"] = kw.get("domaine_is_autre") == "True"
        elif default_domaine_is_autre:
            vals["domaine_is_autre"] = False

        if kw.get("echeance_debut"):
            vals["echeance_debut"] = kw.get("echeance_debut")

        if kw.get("echeance_fin"):
            vals["echeance_fin"] = kw.get("echeance_fin")

        if kw.get("nom_equipe"):
            vals["nom_equipe"] = kw.get("nom_equipe")

        if kw.get("recruteur_id") and kw.get("recruteur_id").isdigit():
            vals["recruteur_id"] = int(kw.get("recruteur_id"))

        if kw.get("role"):
            lst_value_role = [
                (4, int(a)) for a in request.httprequest.form.getlist("role")
            ]
            vals["role"] = lst_value_role

        if kw.get("role_autre"):
            vals["role_autre"] = kw.get("role_autre")

        default_role_is_autre = (
            http.request.env["ceppp.implication"]
            .default_get(["role_is_autre"])
            .get("role_is_autre")
        )
        if kw.get("role_is_autre"):
            vals["role_is_autre"] = kw.get("role_is_autre") == "True"
        elif default_role_is_autre:
            vals["role_is_autre"] = False

        if kw.get("titre"):
            vals["titre"] = kw.get("titre")

        new_ceppp_implication = (
            request.env["ceppp.implication"].sudo().create(vals)
        )
        return werkzeug.utils.redirect(
            f"/my/ceppp_implication/{new_ceppp_implication.id}"
        )

    @http.route("/new/ceppp_maladie", type="http", auth="user", website=True)
    def create_new_ceppp_maladie(self, **kw):
        chapitre_maladie_id = http.request.env[
            "ceppp.chapitre_maladie"
        ].search([])
        default_chapitre_maladie_id = (
            http.request.env["ceppp.maladie"]
            .default_get(["chapitre_maladie_id"])
            .get("chapitre_maladie_id")
        )
        default_nom = (
            http.request.env["ceppp.maladie"].default_get(["nom"]).get("nom")
        )
        return http.request.render(
            "ceppp_patient_partenaire.portal_create_ceppp_maladie",
            {
                "chapitre_maladie_id": chapitre_maladie_id,
                "page_name": "create_ceppp_maladie",
                "default_chapitre_maladie_id": default_chapitre_maladie_id,
                "default_nom": default_nom,
            },
        )

    @http.route(
        "/submitted/ceppp_maladie",
        type="http",
        auth="user",
        website=True,
        csrf=True,
    )
    def submit_ceppp_maladie(self, **kw):
        vals = {}

        if (
            kw.get("chapitre_maladie_id")
            and kw.get("chapitre_maladie_id").isdigit()
        ):
            vals["chapitre_maladie_id"] = int(kw.get("chapitre_maladie_id"))

        if kw.get("nom"):
            vals["nom"] = kw.get("nom")

        new_ceppp_maladie = request.env["ceppp.maladie"].sudo().create(vals)
        return werkzeug.utils.redirect(
            f"/my/ceppp_maladie/{new_ceppp_maladie.id}"
        )

    @http.route(
        "/new/ceppp_maladie_proche_aidant",
        type="http",
        auth="user",
        website=True,
    )
    def create_new_ceppp_maladie_proche_aidant(self, **kw):
        name = http.request.env.user.name
        maladie = http.request.env["ceppp.maladie"].search([])
        lst_default_maladie = (
            http.request.env["ceppp.maladie_proche_aidant"]
            .default_get(["maladie"])
            .get("maladie")
        )
        if lst_default_maladie:
            default_maladie = lst_default_maladie[0][2]
        else:
            default_maladie = []
        recruteur_id = http.request.env["ceppp.recruteur"].search(
            [("active", "=", True)]
        )
        default_recruteur_id = (
            http.request.env["ceppp.maladie_proche_aidant"]
            .default_get(["recruteur_id"])
            .get("recruteur_id")
        )
        relation = http.request.env["ceppp.relation_proche"].search([])
        lst_default_relation = (
            http.request.env["ceppp.maladie_proche_aidant"]
            .default_get(["relation"])
            .get("relation")
        )
        if lst_default_relation:
            default_relation = lst_default_relation[0][2]
        else:
            default_relation = []
        default_relation_autre = (
            http.request.env["ceppp.maladie_proche_aidant"]
            .default_get(["relation_autre"])
            .get("relation_autre")
        )
        default_relation_is_autre = (
            http.request.env["ceppp.maladie_proche_aidant"]
            .default_get(["relation_is_autre"])
            .get("relation_is_autre")
        )
        return http.request.render(
            "ceppp_patient_partenaire.portal_create_ceppp_maladie_proche_aidant",
            {
                "name": name,
                "maladie": maladie,
                "recruteur_id": recruteur_id,
                "relation": relation,
                "page_name": "create_ceppp_maladie_proche_aidant",
                "default_maladie": default_maladie,
                "default_recruteur_id": default_recruteur_id,
                "default_relation": default_relation,
                "default_relation_autre": default_relation_autre,
                "default_autre_maladie": "",
                "default_relation_is_autre": default_relation_is_autre,
            },
        )

    @http.route(
        "/submitted/ceppp_maladie_proche_aidant",
        type="http",
        auth="user",
        website=True,
        csrf=True,
    )
    def submit_ceppp_maladie_proche_aidant(self, **kw):
        vals = {}

        # if kw.get("name"):
        #     vals["name"] = kw.get("name")

        if kw.get("autre_maladie"):
            vals["autre_maladie"] = kw.get("autre_maladie")

        if kw.get("maladie"):
            lst_value_maladie = [
                (4, int(a))
                for a in request.httprequest.form.getlist("maladie")
            ]
            vals["maladie"] = lst_value_maladie

        if kw.get("recruteur_id") and kw.get("recruteur_id").isdigit():
            vals["recruteur_id"] = int(kw.get("recruteur_id"))

        if kw.get("relation"):
            lst_value_relation = [
                (4, int(a))
                for a in request.httprequest.form.getlist("relation")
            ]
            vals["relation"] = lst_value_relation

        if kw.get("relation_autre"):
            vals["relation_autre"] = kw.get("relation_autre")

        default_relation_is_autre = (
            http.request.env["ceppp.maladie_proche_aidant"]
            .default_get(["relation_is_autre"])
            .get("relation_is_autre")
        )
        if kw.get("relation_is_autre"):
            vals["relation_is_autre"] = kw.get("relation_is_autre") == "True"
        elif default_relation_is_autre:
            vals["relation_is_autre"] = False

        new_ceppp_maladie_proche_aidant = (
            request.env["ceppp.maladie_proche_aidant"].sudo().create(vals)
        )
        return werkzeug.utils.redirect(
            f"/my/ceppp_maladie_proche_aidant/{new_ceppp_maladie_proche_aidant.id}"
        )
