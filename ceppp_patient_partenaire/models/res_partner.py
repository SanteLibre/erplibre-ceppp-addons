from odoo import SUPERUSER_ID, _, api, fields, models, tools


class ResPartner(models.Model):
    _inherit = "res.partner"

    ceppp_entity = fields.Selection(
        selection=[
            ("patient", "Patient"),
            ("recruteur", "Recruteur"),
            ("affiliation", "Centre de recrutement"),
            ("administrateur", "Administrateur"),
        ],
        string="Affiliation",
        help="Unique entity name to represent the contact.",
    )
