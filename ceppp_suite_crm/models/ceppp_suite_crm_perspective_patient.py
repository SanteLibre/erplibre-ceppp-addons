from odoo import _, api, fields, models


class CepppSuiteCrmPerspectivePatient(models.Model):
    _name = "ceppp.suite_crm.perspective_patient"
    _description = "ceppp_suite_crm_perspective_patient"
    _rec_name = "adresse_perso_city"

    adresse_perso_city = fields.Char()

    adresse_perso = fields.Char()

    adresse_perso_country = fields.Char()

    adresse_perso_postalcode = fields.Char()

    adresse_perso_state = fields.Char()

    conflit_interet = fields.Boolean()

    conflit_interet_detail = fields.Text()

    descr_exp = fields.Text()

    duree_experience = fields.Char()

    etabl_prem_ligne_pa = fields.Char()

    etabl_sante_pa = fields.Char()

    exp_sante = fields.Boolean()

    exp_sante_detail = fields.Text()

    experience_maladie = fields.Text()

    experience_maladie_pa = fields.Text()

    experience_maladie_proche = fields.Text(
        help="What is your family member's experience with illness?"
    )

    formation_date = fields.Date()

    formation_oui = fields.Char()

    formation_pp = fields.Boolean()

    formation_qui = fields.Char()

    maladie_rare_details = fields.Text()

    med_1 = fields.Text()

    membre_assoc_comite = fields.Boolean()

    membre_assoc_comite_detail = fields.Text()

    motivations_implication = fields.Text()

    perspective = fields.Char()

    preferences_autre = fields.Text()

    preneur_decisions = fields.Text()

    professionnels_sante = fields.Char()
