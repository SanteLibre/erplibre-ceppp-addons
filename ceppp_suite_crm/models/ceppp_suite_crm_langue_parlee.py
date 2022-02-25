from odoo import _, api, fields, models


class CepppSuiteCrmLangueParlee(models.Model):
    _name = "ceppp.suite_crm.langue_parlee"
    _description = "ceppp_suite_crm_langue_parlee"
    _rec_name = "nom"

    nom = fields.Char(translate=True)
