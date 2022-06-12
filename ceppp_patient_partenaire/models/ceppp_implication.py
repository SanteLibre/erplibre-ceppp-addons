from odoo import _, api, fields, models


class CepppImplication(models.Model):
    _name = "ceppp.implication"
    _description = "ceppp_implication"

    name = fields.Char()
