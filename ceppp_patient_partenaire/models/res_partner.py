from odoo import SUPERUSER_ID, _, api, fields, models, tools


class Partner(models.Model):
    _inherit = "res.partner"
    _name = "res.partner"

    patient = fields.Boolean(
        string="Est un patient",
        help="Check this box if this contact is a patient.",
    )
    recruteur = fields.Boolean(
        string="Est un recruteur",
        help="Check this box if this contact is a recruteur.",
    )
