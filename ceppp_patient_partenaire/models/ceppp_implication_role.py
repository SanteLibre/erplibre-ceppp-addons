from odoo import _, api, fields, models


class CepppImplicationRole(models.Model):
    _name = "ceppp.implication_role"
    _description = "ceppp_implication_role"
    _order = "sequence, id"

    name = fields.Char()

    sequence = fields.Integer(default=1, help="Order the list")
