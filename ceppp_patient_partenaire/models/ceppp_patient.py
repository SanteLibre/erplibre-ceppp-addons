from uuid import uuid4

from odoo import _, api, fields, models


class CepppPatient(models.Model):
    _name = "ceppp.patient"
    _description = "ceppp_patient"
    _rec_name = "uuid"

    uuid = fields.Char(related="recruteur_id.uuid")

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

    maladie_personne_affectee = fields.One2many(
        related="recruteur_id.maladie_personne_affectee",
    )

    search_maladie = fields.Char(related="recruteur_id.search_maladie")

    search_implication = fields.Char(related="recruteur_id.search_implication")

    search_formation = fields.Char(related="recruteur_id.search_formation")

    formation = fields.One2many(
        related="recruteur_id.formation",
    )

    implication = fields.One2many(
        related="recruteur_id.implication",
    )

    user_is_manager = fields.Boolean(
        store=False,
        compute="_compute_user_is_manager",
    )

    @api.depends("recruteur_id")
    def _compute_user_is_manager(self):
        for record in self:
            record.user_is_manager = (
                self.env["res.users"].browse(self._uid).partner_id.ceppp_entity
                == "administrateur"
            ) or self.recruteur_partner_id == self.env.user.partner_id

    def open_fiche_recruteur(self):
        return {
            "name": _("Fiche recruteur"),
            "res_model": "ceppp.recruteur",
            "view_type": "form",
            "view_mode": "form",
            "type": "ir.actions.act_window",
            "res_id": self.recruteur_id.id,
        }
