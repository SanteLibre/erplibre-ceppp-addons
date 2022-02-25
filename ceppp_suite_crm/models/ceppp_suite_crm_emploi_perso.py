from odoo import _, api, fields, models


class CepppSuiteCrmEmploiPerso(models.Model):
    _name = "ceppp.suite_crm.emploi_perso"
    _description = "ceppp_suite_crm_emploi_perso"
    _rec_name = "nom"

    nom = fields.Char(translate=True)
