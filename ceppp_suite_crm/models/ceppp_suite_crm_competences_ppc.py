from odoo import _, api, fields, models


class CepppSuiteCrmCompetencesPpc(models.Model):
    _name = "ceppp.suite_crm.competences_ppc"
    _description = "ceppp_suite_crm_competences_ppc"
    _rec_name = "nom"

    nom = fields.Char(translate=True)
