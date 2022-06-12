from odoo import _, api, fields, models


class CepppMaladieSoiMeme(models.Model):
    _name = "ceppp.maladie_soi_meme"
    _description = "ceppp_maladie_soi_meme"

    name = fields.Char()
