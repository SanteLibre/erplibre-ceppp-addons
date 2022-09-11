from odoo import _, api, fields, models


class CepppDisponibilite(models.Model):
    _name = "ceppp.disponibilite"
    _description = "ceppp_disponibilite"

    name = fields.Char()
