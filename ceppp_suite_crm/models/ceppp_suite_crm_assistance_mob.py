from odoo import _, api, fields, models


class CepppSuiteCrmAssistanceMob(models.Model):
    _name = "ceppp.suite_crm.assistance_mob"
    _description = "ceppp_suite_crm_assistance_mob"
    _rec_name = "nom"

    nom = fields.Char(translate=True)
