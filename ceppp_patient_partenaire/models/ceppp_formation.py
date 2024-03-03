from odoo import _, api, fields, models


class CepppFormation(models.Model):
    _name = "ceppp.formation"
    _description = "ceppp_formation"

    name = fields.Char(compute="_compute_name")

    titre_formation = fields.Many2many(
        comodel_name="ceppp.formation_titre",
        string="Titre de la formation",
    )

    titre_formation_autre = fields.Char(string="Autres formations")

    organisation = fields.Char(
        help="Quelles organisations a donné cette formation?"
    )

    recruteur_id = fields.Many2one(
        comodel_name="ceppp.recruteur",
    )

    date = fields.Date(
        string="Date début",
        help=(
            "Quelle est la date de cette formation? Si vous ne vous en"
            " souvenez pas, veuillez indiquer la première journée du mois (ex."
            " 1 mai 2022) ou la première journée de l'année si vous ne vous"
            " rappellez plus du mois (ex. 1 janvier 2022)."
        ),
    )

    date_fin = fields.Date(
        string="Date fin",
        help=(
            "Si la date est différente de celle de début, ou que la formation"
            " est sur plusieurs jours."
        ),
    )

    titre_formation_is_autre = fields.Boolean(
        compute="_compute_titre_formation_is_autre"
    )

    @api.depends("titre_formation")
    def _compute_titre_formation_is_autre(self):
        for record in self:
            record.titre_formation_is_autre = (
                self.env.ref(
                    "ceppp_patient_partenaire.ceppp_formation_titre_6"
                ).id
                in record.titre_formation.ids
            )

    @api.depends(
        "titre_formation", "titre_formation_autre", "titre_formation_is_autre"
    )
    def _compute_name(self):
        for record in self:
            id_autre = self.env.ref(
                "ceppp_patient_partenaire.ceppp_formation_titre_6"
            ).id
            lst_formation = [
                a.name for a in record.titre_formation if a.id != id_autre
            ]
            if (
                record.titre_formation_is_autre
                and record.titre_formation_autre
            ):
                lst_formation += [record.titre_formation_autre]
            record.name = ";".join(lst_formation)

    @api.multi
    def update_formation_portal(self, values):
        titre_formation = [(6, 0, [int(a) for a in values["titre_formation"]])]
        maladie_values = {
            "organisation": values["organisation"],
            "date": values["date"] or False,
            "date_fin": values["date_fin"] or False,
            "titre_formation": titre_formation,
            "titre_formation_autre": values["titre_formation_autre"],
        }
        self.write(maladie_values)
