from odoo import _, api, fields, models


class CepppImplicationRole(models.Model):
    _name = "ceppp.implication_role"
    _description = "ceppp_implication_role"

    name = fields.Char()
