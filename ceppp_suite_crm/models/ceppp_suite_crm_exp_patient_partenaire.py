from odoo import _, api, fields, models


class CepppSuiteCrmExpPatientPartenaire(models.Model):
    _name = "ceppp.suite_crm.exp_patient_partenaire"
    _description = "ceppp_suite_crm_exp_patient_partenaire"

    name = fields.Char(required=True)

    comite = fields.Char()

    date_formation = fields.Date()

    description_experience = fields.Text()

    duree = fields.Char()

    formation_qui = fields.Char()

    formation_suivie = fields.Boolean()

    nom_formation_suivie = fields.Char()
