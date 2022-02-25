from odoo import _, api, fields, models


class CepppSuiteCrmRolePp(models.Model):
    _name = "ceppp.suite_crm.role_pp"
    _description = "ceppp_suite_crm_role_pp"
    _rec_name = "nom"

    nom = fields.Char(translate=True)
