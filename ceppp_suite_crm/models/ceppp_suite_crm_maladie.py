from odoo import _, api, fields, models


class CepppSuiteCrmMaladie(models.Model):
    _name = "ceppp.suite_crm.maladie"
    _description = "ceppp_suite_crm_maladie"
    _rec_name = "nom"

    nom = fields.Char()

    chapitre_maladie_id = fields.Many2one(
        comodel_name="ceppp.suite_crm.chapitre_maladie",
        string="Chapitre maladie",
    )
