from odoo import _, api, fields, models


class CepppSuiteCrmPerspectivePatient(models.Model):
    _name = "ceppp.suite_crm.perspective_patient"
    _description = "ceppp_suite_crm_perspective_patient"
    _rec_name = "adresse_perso_city"

    adresse_perso_city = fields.Char(string="Ville")

    adresse_perso = fields.Char(string="Adresse")

    adresse_perso_country = fields.Char(string="Pays")

    adresse_perso_postalcode = fields.Char(string="Code postal")

    adresse_perso_state = fields.Char(string="Province")

    conflit_interet = fields.Boolean(string="Conflits d'intérêt")

    conflit_interet_detail = fields.Text(string="Lesquels")

    descr_exp = fields.Text(string="Description de l'expérience")

    duree_experience = fields.Char(string="Durée d'expérience (Années / Mois)")

    etabl_prem_ligne_pa = fields.Char(string="Établissement de première ligne")

    etabl_sante_pa = fields.Char(string="Établissement de santé principal")

    exp_decision = fields.Selection(
        selection=[("dunno", "Je ne sais pas"), ("yes", "Oui"), ("no", "Non")],
        string="Expérience prise de décision relative à ses soins médicaux",
    )

    exp_sante = fields.Boolean(
        string="Expérience professionnelle dans le milieu de la santé"
    )

    exp_sante_detail = fields.Text(string="Précisions")

    experience_maladie = fields.Text(string="Expérience maladie")

    experience_maladie_pa = fields.Text(string="Expérience comme pair aidant")

    experience_maladie_proche = fields.Text(
        string="Expérience maladie proche",
        help="What is your family member's experience with illness?",
    )

    formation_date = fields.Date(string="Date de formation")

    formation_oui = fields.Char(string="Si oui, laquelle")

    formation_pp = fields.Boolean(
        string="Formation suivie sur le partenariat patient"
    )

    formation_qui = fields.Char(string="Formation par qui")

    maladie_rare_details = fields.Text(string="Maladie rare")

    med_1 = fields.Text(string="Médicaments")

    membre_assoc_comite = fields.Boolean(
        string="Membre d'une association ou comité"
    )

    membre_assoc_comite_detail = fields.Text(string="Laquelle")

    motivations_implication = fields.Text(string="Motivations à s'impliquer")

    perspective = fields.Char()

    preferences_autre = fields.Text(string="Autres préférences")

    preneur_decisions = fields.Text(string="Preneur de décisions")

    professionnels_sante = fields.Char(string="Professionnels de la santé")
