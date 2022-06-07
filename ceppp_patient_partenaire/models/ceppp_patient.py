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

    sexe = fields.Selection(
        selection=[
            ("homme", "Homme"),
            ("femme", "Femme"),
            ("intersexe", "Intersexe"),
            ("no", "Préfère ne pas répondre"),
        ],
        help=(
            "Le sexe fait référence à un ensemble de caractéristiques"
            " biologiques chez les humains et les animaux. Ces"
            " caractéristiques physiques ou physiologiques concernent"
            " principalement les chromosomes, l’expression des gènes, les"
            " niveaux d’hormones et leur fonction, ainsi que l’anatomie de"
            " l’appareil reproducteur. Le sexe comporte habituellement deux"
            " catégories (mâle, femelle); cependant, les caractéristiques"
            " biologiques liées au sexe et l’expression de ces"
            " caractéristiques peuvent varier."
        ),
        default="no",
        required=True,
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if "uuid" not in vals.keys():
                vals["uuid"] = str(uuid4())
        return super(CepppPatient, self).create(vals_list)
