from odoo import _, api, fields, models


class CepppSuiteCrmCompetencesPr(models.Model):
    _name = "ceppp.suite_crm.competences_pr"
    _description = "ceppp_suite_crm_competences_pr"
    _rec_name = "nom"

    nom = fields.Char(translate=True)
