from odoo import _, api, fields, models


class CepppSuiteCrmFormation(models.Model):
    _name = "ceppp.suite_crm.formation"
    _description = "ceppp_suite_crm_formation"
    _rec_name = "formation_par_qui"

    formation_par_qui = fields.Char()

    date_formation = fields.Date()

    exp_sante = fields.Boolean()

    exp_sante_details = fields.Text()
