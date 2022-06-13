from odoo import _, api, fields, models


class CepppRelationProche(models.Model):
    _name = "ceppp.relation_proche"
    _description = "ceppp_relation_proche"

    name = fields.Char()
