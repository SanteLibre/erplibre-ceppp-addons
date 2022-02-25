from odoo import _, api, fields, models


class CepppSuiteCrmDeplacements(models.Model):
    _name = "ceppp.suite_crm.deplacements"
    _description = "ceppp_suite_crm_deplacements"
    _rec_name = "nom"

    nom = fields.Char(translate=True)
