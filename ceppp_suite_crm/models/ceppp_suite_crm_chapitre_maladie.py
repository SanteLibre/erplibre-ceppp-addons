from odoo import _, api, fields, models


class CepppSuiteCrmChapitreMaladie(models.Model):
    _name = "ceppp.suite_crm.chapitre_maladie"
    _description = "ceppp_suite_crm_chapitre_maladie"
    _rec_name = "nom"

    nom = fields.Char()
