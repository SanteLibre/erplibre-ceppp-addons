from odoo import _, api, fields, models


class CepppMaladie(models.Model):
    _name = "ceppp.maladie"
    _description = "ceppp_maladie"
    _rec_name = "nom"

    nom = fields.Char(translate=True)

    chapitre_maladie_id = fields.Many2one(
        comodel_name="ceppp.chapitre_maladie",
        string="Chapitre maladie",
    )
