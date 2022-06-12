from odoo import _, api, fields, models


class CepppRecruteur(models.Model):
    _name = "ceppp.recruteur"
    _description = "ceppp_recruteur"

    name = fields.Char(related="patient_id.name")

    patient_id = fields.Many2one(
        "ceppp.patient",
        string="Patient",
    )
