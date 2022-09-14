from odoo import _, api, fields, models


class CepppDisponibilite(models.Model):
    _name = "ceppp.disponibilite"
    _description = "ceppp_disponibilite"
    _order = "sequence, id"

    name = fields.Char()

    sequence = fields.Integer(default=1, help="Order the list")
