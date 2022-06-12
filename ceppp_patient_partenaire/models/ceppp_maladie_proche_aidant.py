from odoo import _, api, fields, models


class CepppMaladieProcheAidant(models.Model):
    _name = "ceppp.maladie_proche_aidant"
    _description = "ceppp_maladie_proche_aidant"

    name = fields.Char()
