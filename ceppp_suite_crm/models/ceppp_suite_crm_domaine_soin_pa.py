from odoo import _, api, fields, models


class CepppSuiteCrmDomaineSoinPa(models.Model):
    _name = "ceppp.suite_crm.domaine_soin_pa"
    _description = "ceppp_suite_crm_domaine_soin_pa"
    _rec_name = "nom"

    nom = fields.Char(translate=True)
