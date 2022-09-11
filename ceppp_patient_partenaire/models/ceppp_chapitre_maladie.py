from odoo import _, api, fields, models


class CepppChapitreMaladie(models.Model):
    _name = "ceppp.chapitre_maladie"
    _description = "ceppp_chapitre_maladie"
    _rec_name = "nom"

    nom = fields.Char(translate=True)

    maladie_ids = fields.One2many(
        comodel_name="ceppp.maladie",
        inverse_name="chapitre_maladie_id",
        string="Maladies",
    )
