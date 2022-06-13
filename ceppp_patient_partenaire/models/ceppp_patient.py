from uuid import uuid4

from odoo import _, api, fields, models


class CepppPatient(models.Model):
    _name = "ceppp.patient"
    _description = "ceppp_patient"
    _rec_name = "uuid"

    uuid = fields.Char(related="recruteur_id.uuid")

    consentement_notification = fields.Boolean(
        related="recruteur_id.consentement_notification"
    )

    consentement_recrutement = fields.Boolean(
        related="recruteur_id.consentement_recrutement"
    )

    consentement_recherche = fields.Boolean(
        related="recruteur_id.consentement_recherche"
    )

    disponibilite = fields.Many2many(related="recruteur_id.disponibilite")

    disponibilite_not = fields.Many2many(
        related="recruteur_id.disponibilite_not"
    )

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
