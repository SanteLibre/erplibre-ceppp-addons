from odoo import _, api, fields, models


class CepppSuiteCrmEntrevues(models.Model):
    _name = "ceppp.suite_crm.entrevues"
    _description = "ceppp_suite_crm_entrevues"
    _rec_name = "comment_refere"

    comment_refere = fields.Char(
        string="Comment",
        help="Comment avez-vous été référé?",
    )

    date_entrevue = fields.Date(
        string="Date d'entrevue",
        help="Date de la rencontre téléphonique",
    )

    org_ref_recrut = fields.Char(
        string="Établissement de recrutement",
        help="Quel organisme?",
    )
