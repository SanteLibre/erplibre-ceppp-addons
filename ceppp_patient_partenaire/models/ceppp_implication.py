from odoo import _, api, fields, models


class CepppImplication(models.Model):
    _name = "ceppp.implication"
    _description = "ceppp_implication"

    name = fields.Char(string="Nom", compute="_compute_name")

    titre = fields.Char(string="Titre du projet")

    nom_equipe = fields.Char(string="Nom de l'équipe")

    description = fields.Text(
        help="Description générale projet + tâches patients partenaires"
    )

    role = fields.Many2many(
        comodel_name="ceppp.implication_role",
        string="Rôle",
        help="Rôle au sein de ce projet/cette équipe.",
    )

    role_autre = fields.Char(string="Autres rôles")

    domaine = fields.Many2many(
        comodel_name="ceppp.implication_domaine",
        help="Domaine d'implication",
    )

    domaine_autre = fields.Char(string="Autres domaines")

    echeance_debut = fields.Date(
        string="Échéance début",
        help="Période de début du projet",
    )

    echeance_fin = fields.Date(
        string="Échéance fin",
        help="Période de fin du projet",
    )

    recruteur_id = fields.Many2one(
        comodel_name="ceppp.recruteur",
        string="Recruteur",
    )

    role_is_autre = fields.Boolean(compute="_compute_role_is_autre")

    @api.depends("role")
    def _compute_role_is_autre(self):
        for record in self:
            record.role_is_autre = (
                self.env.ref(
                    "ceppp_patient_partenaire.ceppp_implication_role_5"
                ).id
                in record.role.ids
            )

    domaine_is_autre = fields.Boolean(compute="_compute_domaine_is_autre")

    @api.depends("domaine")
    def _compute_domaine_is_autre(self):
        for record in self:
            record.domaine_is_autre = (
                self.env.ref(
                    "ceppp_patient_partenaire.ceppp_implication_domaine_8"
                ).id
                in record.domaine.ids
            )

    @api.depends("titre")
    def _compute_name(self):
        for record in self:
            record.name = record.titre

    @api.multi
    def update_implication_portal(self, values):
        domaine = [(6, 0, [int(a) for a in values["domaine"]])]
        role = [(6, 0, [int(a) for a in values["role"]])]
        implication_values = {
            "titre": values["titre"],
            "nom_equipe": values["nom_equipe"],
            "description": values["description"],
            "echeance_debut": values["echeance_debut"] or False,
            "echeance_fin": values["echeance_fin"] or False,
            "domaine": domaine,
            "domaine_autre": values["domaine_autre"],
            "role": role,
            "role_autre": values["role_autre"],
        }
        self.write(implication_values)
