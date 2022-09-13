from odoo import _, api, fields, models


class CepppFormationTitre(models.Model):
    _name = "ceppp.formation_titre"
    _description = "ceppp_formation_titre"
    _order = "sequence, id"

    name = fields.Char()

    sequence = fields.Integer(default=1, help="Order the list")
