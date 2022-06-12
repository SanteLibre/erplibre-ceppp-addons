from odoo import _, api, fields, models


class CepppRecruteur(models.Model):
    _name = "ceppp.recruteur"
    _description = "ceppp_recruteur"

    name = fields.Char()
