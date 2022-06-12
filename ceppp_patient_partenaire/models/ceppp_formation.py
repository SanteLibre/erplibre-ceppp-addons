from odoo import _, api, fields, models


class CepppFormation(models.Model):
    _name = "ceppp.formation"
    _description = "ceppp_formation"

    name = fields.Char()
