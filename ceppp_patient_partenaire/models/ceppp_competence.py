from odoo import _, api, fields, models


class CepppCompetence(models.Model):
    _name = "ceppp.competence"
    _description = "ceppp_competence"
    _order = "sequence, id"

    name = fields.Char()

    sequence = fields.Integer(default=1, help="Order the list")
