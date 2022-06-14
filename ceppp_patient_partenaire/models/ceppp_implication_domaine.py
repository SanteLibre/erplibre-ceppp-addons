from odoo import _, api, fields, models


class CepppImplicationDomaine(models.Model):
    _name = "ceppp.implication_domaine"
    _description = "ceppp_implication_domaine"

    name = fields.Char()
