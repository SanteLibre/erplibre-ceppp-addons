from odoo import _, api, fields, models


class CepppFormationTitre(models.Model):
    _name = "ceppp.formation_titre"
    _description = "ceppp_formation_titre"

    name = fields.Char()
