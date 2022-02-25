from odoo import _, api, fields, models


class CepppSuiteCrmCompetencesPp(models.Model):
    _name = "ceppp.suite_crm.competences_pp"
    _description = "ceppp_suite_crm_competences_pp"
    _rec_name = "nom"

    nom = fields.Char(translate=True)
