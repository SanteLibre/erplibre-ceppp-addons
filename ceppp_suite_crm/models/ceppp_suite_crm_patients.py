from odoo import _, api, fields, models


class CepppSuiteCrmPatients(models.Model):
    _name = "ceppp.suite_crm.patients"
    _description = "ceppp_suite_crm_patients"
    _rec_name = "nas_perso_"

    nas_perso_ = fields.Char()

    assistance_audition = fields.Boolean()

    assistance_vision = fields.Boolean()

    centre_recrutement = fields.Char()

    code_ident = fields.Char(required=True)

    comm_recruteur = fields.Text()

    comment_refere = fields.Char()

    conflit_interet = fields.Boolean()

    conflit_interet_detail = fields.Char()

    consentement_dcpp_recrut = fields.Boolean()

    consentement_miseajour = fields.Boolean()

    consentement_recherche = fields.Boolean()

    consentement_usage_donnees = fields.Boolean()

    date_entrevue = fields.Date()

    descr_exp = fields.Char()

    doul_chron = fields.Boolean()

    duree_experience = fields.Char()

    education_perso_autre = fields.Char()

    email_perso = fields.Char()

    etabl_prem_ligne_pa_ = fields.Char()

    etabl_sante_pa_ = fields.Char()

    exp_sante = fields.Boolean()

    exp_sante_detail = fields.Text()

    experience_maladie_pa = fields.Text()

    experience_maladie_pp = fields.Text()

    experience_maladie_proche = fields.Text()

    formation_date = fields.Date()

    formation_oui = fields.Char()

    formation_pp = fields.Boolean()

    formation_qui = fields.Char()

    membre_assoc_comite = fields.Boolean()

    membre_assoc_comite_detail = fields.Char()

    motivations_implication = fields.Char()

    naissance_perso = fields.Date(required=True)

    nas_perso = fields.Integer()

    niveau_aud = fields.Boolean()

    niveau_autre = fields.Char()

    niveau_fatigabilite = fields.Boolean()

    niveau_mob = fields.Boolean()

    niveau_vue = fields.Boolean()

    nom = fields.Char()

    org_ref_recrut = fields.Char()

    patient_ajout = fields.Text()

    personne_reference_recrut = fields.Char()

    preferences_autre = fields.Text()

    prenom = fields.Char()

    prob_resp = fields.Boolean()

    prob_somm = fields.Boolean()

    recruteur = fields.Char()

    tel_dom_perso = fields.Char()

    tel_mobile_perso = fields.Char()

    tel_travail_perso = fields.Char()

    test_int_field = fields.Integer()
