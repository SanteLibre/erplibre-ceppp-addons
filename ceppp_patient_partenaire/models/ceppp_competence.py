from odoo import _, api, fields, models


class CepppCompetence(models.Model):
    _name = "ceppp.competence"
    _description = "ceppp_competence"

    name = fields.Char()
