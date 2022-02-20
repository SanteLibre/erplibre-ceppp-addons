from odoo import _, api, fields, models


class CepppSuiteCrmCommentairesRecruteur(models.Model):
    _name = "ceppp.suite_crm.commentaires_recruteur"
    _description = "ceppp_suite_crm_commentaires_recruteur"
    _rec_name = "commentaires_recruteur"

    commentaires_recruteur = fields.Text()
