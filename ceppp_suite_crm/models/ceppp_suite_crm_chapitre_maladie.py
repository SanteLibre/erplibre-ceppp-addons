from odoo import _, api, fields, models


class CepppSuiteCrmChapitreMaladie(models.Model):
    _name = "ceppp.suite_crm.chapitre_maladie"
    _description = "ceppp_suite_crm_chapitre_maladie"
    _rec_name = "nom"

    nom = fields.Char()

    maladie_ids = fields.One2many(
        comodel_name="ceppp.suite_crm.maladie",
        inverse_name="chapitre_maladie_id",
        string="Maladies",
    )
