from odoo import _, api, fields, models


class CepppOccupation(models.Model):
    _name = "ceppp.occupation"
    _description = "ceppp_occupation"

    name = fields.Char()
