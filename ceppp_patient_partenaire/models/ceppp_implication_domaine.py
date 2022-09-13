from odoo import _, api, fields, models


class CepppImplicationDomaine(models.Model):
    _name = "ceppp.implication_domaine"
    _description = "ceppp_implication_domaine"
    _order = "sequence, id"

    name = fields.Char()

    sequence = fields.Integer(default=1, help="Order the list")
