from odoo import _, api, fields, models


class CepppSuiteCrmFormation(models.Model):
    _name = "ceppp.suite_crm.formation"
    _description = "ceppp_suite_crm_formation"
    _rec_name = "formation_par_qui"

    formation_par_qui = fields.Char(string="Par qui")

    date_formation = fields.Date(string="Date de formation")

    exp_sante = fields.Boolean(
        string="Expérience professionnelle dans le milieu de la santé"
    )

    exp_sante_details = fields.Text(string="Détails")
