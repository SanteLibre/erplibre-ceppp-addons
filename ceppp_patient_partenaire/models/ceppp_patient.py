from uuid import uuid4

from odoo import _, api, fields, models


class CepppPatient(models.Model):
    _name = "ceppp.patient"
    _description = "ceppp_patient"
    _rec_name = "uuid"

    name = fields.Char(
        related="partner_id.name",
        groups=(
            "ceppp_patient_partenaire.group_ceppp_patient_partenaire_manager"
        ),
    )

    uuid = fields.Char(string="Code", help="Identifiant unique anonymisé.")

    partner_id = fields.Many2one(
        "res.partner",
        string="Patient",
        groups=(
            "ceppp_patient_partenaire.group_ceppp_patient_partenaire_manager"
        ),
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if "uuid" not in vals.keys():
                vals["uuid"] = str(uuid4())
        return super(CepppPatient, self).create(vals_list)
