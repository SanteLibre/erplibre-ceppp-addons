from uuid import uuid4

from odoo import _, api, fields, models


class CepppPatient(models.Model):
    _name = "ceppp.patient"
    _description = "ceppp_patient"
    _rec_name = "uuid"

    uuid = fields.Char(related="recruteur_id.uuid")

    name = fields.Char(related="recruteur_id.name")

    recruteur_id = fields.Many2one(
        comodel_name="ceppp.recruteur",
        string="Link recruteur",
    )

    recruteur_partner_id = fields.Many2one(
        related="recruteur_id.recruteur_partner_id"
    )

    centre_recruteur = fields.Char(
        related="recruteur_id.centre_recruteur",
    )
