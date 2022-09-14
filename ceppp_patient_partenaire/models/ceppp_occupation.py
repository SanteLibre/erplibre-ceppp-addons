from odoo import _, api, fields, models


class CepppOccupation(models.Model):
    _name = "ceppp.occupation"
    _description = "ceppp_occupation"
    _order = "sequence, id"

    name = fields.Char()

    sequence = fields.Integer(default=1, help="Order the list")
