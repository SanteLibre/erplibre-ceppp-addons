from odoo import SUPERUSER_ID, _, api, fields, models, tools


class Partner(models.Model):
    _inherit = "res.partner"
    _name = "res.partner"

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
