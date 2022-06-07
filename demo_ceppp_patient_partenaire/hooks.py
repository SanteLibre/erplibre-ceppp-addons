# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import base64
import logging

from odoo import SUPERUSER_ID, _, api, tools

_logger = logging.getLogger(__name__)


def post_init_hook(cr, e):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})

        # Update all partner
        partners = env["res.partner"].search([("name", "=", "My Company")])
        for partner in partners:
            partner.website = "https://ceppp.ca"
            partner.name = "CEPPP"
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
            partner_img_attachment = env.ref(
                "ceppp_patient_partenaire.ir_attachment_logo_ceppp_svg"
            )
            with tools.file_open(
                partner_img_attachment.local_url[1:], "rb"
            ) as desc_file:
                partner.image = base64.b64encode(desc_file.read())
            print("fi")
