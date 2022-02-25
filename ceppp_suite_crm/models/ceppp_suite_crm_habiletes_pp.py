from odoo import _, api, fields, models


class CepppSuiteCrmHabiletesPp(models.Model):
    _name = "ceppp.suite_crm.habiletes_pp"
    _description = "ceppp_suite_crm_habiletes_pp"
    _rec_name = "nom"

    nom = fields.Char(translate=True)
