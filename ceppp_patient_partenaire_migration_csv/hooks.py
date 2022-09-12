# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import base64
import logging

from odoo import SUPERUSER_ID, _, api, tools

_logger = logging.getLogger(__name__)


def pre_init_hook(cr):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})

        # Update all partner
        partners = env["res.partner"].search([("name", "=", "My Company")])
        for partner in partners:
            partner.website = "https://ceppp.ca"
            partner.name = "CEPPP"
            partner.ceppp_entity = "affiliation"
            partner.email = "info@ceppp.ca"
            partner.street = "850, rue St-Denis"
            partner.street2 = "porte S03.900"
            partner.city = "Montréal"
            partner.zip = "H2X 0A9"
            partner.country_id = env.ref("base.ca")
            partner.state_id = env["res.country.state"].search(
                [("code", "ilike", "QC")], limit=1
            )
            partner.phone = "514 890-8000 poste 15488"

        partners = env["res.partner"].search([("name", "=", "Administrator")])
        for partner in partners:
            partner.website = "https://santelibre.ca"
            partner.name = "Mathieu Benoit"
            partner.email = "mathieu.benoit@santelibre.ca"
            partner.country_id = env.ref("base.ca")
            partner.state_id = env["res.country.state"].search(
                [("code", "ilike", "QC")], limit=1
            )
            partner.ceppp_entity = "administrateur"

        # Take super admin user
        users = env["res.users"].browse(2)
        users.groups_id = [
            (
                4,
                env.ref(
                    "ceppp_patient_partenaire.group_ceppp_patient_partenaire_manager"
                ).id,
            )
        ]


def post_init_hook(cr, e):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})

        # Update all partner
        partners = env["res.partner"].search([("name", "=", "CEPPP")])
        for partner in partners:
            partner_img_attachment = env.ref(
                "ceppp_patient_partenaire.ir_attachment_logo_ceppp_svg"
            )
            with tools.file_open(
                partner_img_attachment.local_url[1:], "rb"
            ) as desc_file:
                partner.image = base64.b64encode(desc_file.read())

        value_genevieve = {
            "parent_id": partners.id,
            "name": "Geneviève David",
            "company_id": env.ref("base.main_company").id,
            "ceppp_entity": "administrateur",
            "customer": False,
            "email": "genevieve.david@ceppp.ca",
            "state_id": env["res.country.state"]
            .search([("code", "ilike", "QC")])
            .id,
            "country_id": env.ref("base.ca").id,
            "tz": "America/Montreal",
        }
        with tools.file_open(
            "ceppp_patient_partenaire_migration_csv/static/img/genevieve_david.jpg",
            "rb",
        ) as desc_file:
            value_genevieve["image"] = base64.b64encode(desc_file.read())

        partner_id_genevieve = env["res.partner"].create(value_genevieve)

        value_genevieve = {
            "login": "genevieve.david@ceppp.ca",
            "company_id": env.ref("base.main_company").id,
            "partner_id": partner_id_genevieve.id,
            "groups_id": [
                (
                    4,
                    env.ref(
                        "ceppp_patient_partenaire.group_ceppp_patient_partenaire_manager"
                    ).id,
                ),
                (4, env.ref("base.user_root").id),
                (4, env.ref("base.user_admin").id),
            ],
        }
        user_id_genevieve = env["res.users"].create(value_genevieve)

        value_santelibre = {
            "name": "SantéLibre",
            "company_id": env.ref("base.main_company").id,
            "customer": False,
            "supplier": True,
            "is_company": True,
            "state_id": env["res.country.state"]
            .search([("code", "ilike", "QC")])
            .id,
            "country_id": env.ref("base.ca").id,
            "tz": "America/Montreal",
        }
        with tools.file_open(
            "ceppp_patient_partenaire_migration_csv/static/img/logo_santelibre.png",
            "rb",
        ) as desc_file:
            value_santelibre["image"] = base64.b64encode(desc_file.read())
        partner_id_santelibre = env["res.partner"].create(value_santelibre)

        partners = env["res.partner"].search([("name", "=", "Mathieu Benoit")])
        for partner in partners:
            partner.parent_id = partner_id_santelibre.id
            with tools.file_open(
                "ceppp_patient_partenaire_migration_csv/static/img/Mathieu_Benoit.jpg",
                "rb",
            ) as desc_file:
                partner.image = base64.b64encode(desc_file.read())
