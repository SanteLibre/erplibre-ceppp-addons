from odoo import _, api, fields, models


class CepppLangue(models.Model):
    _name = "ceppp.langue"
    _description = "ceppp_langue"

    name = fields.Char()
