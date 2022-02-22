from odoo import _, api, fields, models


class CepppSuiteCrmExpPatientPartenaire(models.Model):
    _name = "ceppp.suite_crm.exp_patient_partenaire"
    _description = "ceppp_suite_crm_exp_patient_partenaire"

    name = fields.Char(
        string="Nom",
        required=True,
    )

    comite = fields.Char(string="Comité / Groupe")

    date_formation = fields.Date(string="Date de formation")

    description_experience = fields.Text(string="Description de l'expérience")

    duree = fields.Char(string="Durée")

    formation_qui = fields.Char(string="Formation par qui")

    formation_suivie = fields.Selection(
        selection=[("oui", "Oui"), ("non", "Non")],
        string="Formation suivie sur le partenariat patient",
    )

    nom_formation_suivie = fields.Char(string="nom formation suivie")

    role_experience = fields.Selection(
        selection=[
            ("coach", "Coach"),
            ("co_chercheur", "Co-chercheur"),
            ("formateur", "Formateur"),
            ("accompagnateur", "Accompagnateur"),
            ("aviseur", "Aviseur"),
        ],
        string="Rôle",
    )
