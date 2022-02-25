from odoo import _, api, fields, models


class CepppSuiteCrmMed2(models.Model):
    _name = "ceppp.suite_crm.med_2"
    _description = "ceppp_suite_crm_med_2"
    _rec_name = "nom"

    nom = fields.Char(translate=True)
