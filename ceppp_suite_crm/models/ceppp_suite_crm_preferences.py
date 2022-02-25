from odoo import _, api, fields, models


class CepppSuiteCrmPreferences(models.Model):
    _name = "ceppp.suite_crm.preferences"
    _description = "ceppp_suite_crm_preferences"
    _rec_name = "nom"

    nom = fields.Char(translate=True)
