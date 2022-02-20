from odoo import _, api, fields, models


class CepppSuiteCrmEntrevues(models.Model):
    _name = "ceppp.suite_crm.entrevues"
    _description = "ceppp_suite_crm_entrevues"
    _rec_name = "comment_refere"

    comment_refere = fields.Char(help="Comment avez-vous été référé? ")

    date_entrevue = fields.Date(help="Date de la rencontre téléphonique")

    org_ref_recrut = fields.Char(help="Quel organisme?")
