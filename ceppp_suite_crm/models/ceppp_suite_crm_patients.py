from odoo import _, api, fields, models


class CepppSuiteCrmPatients(models.Model):
    _name = "ceppp.suite_crm.patients"
    _description = "ceppp_suite_crm_patients"
    _rec_name = "nom"

    nom = fields.Char(string="Nom de famille")

    assistance_audition = fields.Boolean(string="Besoin d'assistance")

    assistance_vision = fields.Boolean(string="Besoin d'assistance")

    centre_recrutement = fields.Char(string="Centre de recrutement")

    code_ident = fields.Char(
        string="Code",
        required=True,
    )

    comm_recruteur = fields.Text(string="Commentaires recruteur")

    comment_refere = fields.Char(string="Comment")

    conflit_interet = fields.Boolean(string="Conflit d'intérêt")

    conflit_interet_detail = fields.Char(string="Lequel")

    consentement_dcpp_recrut = fields.Boolean(
        string="Consentement sur l'implication"
    )

    consentement_miseajour = fields.Boolean(
        string="Consentement sur la communication"
    )

    consentement_recherche = fields.Boolean(
        string="Consentement sur la recherche"
    )

    consentement_usage_donnees = fields.Boolean(
        string="Consentement sur les données"
    )

    date_entrevue = fields.Date(string="Date de la rencontre téléphonique")

    descr_exp = fields.Char(string="Description de l'expérience")

    doul_chron = fields.Boolean(string="Douleur chronique")

    duree_experience = fields.Char(string="Durée d'expérience (Années / Mois)")

    education_perso_autre = fields.Char(string="Autre niveau (préciser)")

    email_perso = fields.Char(string="Adresse courriel")

    etabl_prem_ligne_pa_ = fields.Char(
        string="Établissement de première ligne"
    )

    etabl_sante_pa_ = fields.Char(string="Établissement de santé principal")

    exp_sante = fields.Boolean(
        string="Expérience professionnelle dans le milieu de la santé"
    )

    exp_sante_detail = fields.Text(string="Précisions")

    experience_maladie_pa = fields.Text(string="Expérience comme pair aidant")

    experience_maladie_pp = fields.Text(string="Description de l'expérience")

    experience_maladie_proche = fields.Text(string="Expérience maladie proche")

    formation_date = fields.Date(string="Date de formation")

    formation_oui = fields.Char(string="Si oui, laquelle")

    formation_pp = fields.Boolean(
        string="Formation suivie sur le partenariat patient"
    )

    formation_qui = fields.Char(string="Formation par qui")

    membre_assoc_comite = fields.Boolean(
        string="Membre d'une association ou comité"
    )

    membre_assoc_comite_detail = fields.Char(string="Laquelle")

    motivations_implication = fields.Char(string="Motivations à s'impliquer")

    naissance_perso = fields.Date(
        string="Date de naissance",
        required=True,
    )

    nas_perso = fields.Integer()

    nas_perso_ = fields.Char(string="Numéro d'assurance social")

    niveau_aud = fields.Boolean(string="Ouïe")

    niveau_autre = fields.Char(string="Autres besoins spécifiques")

    niveau_fatigabilite = fields.Boolean(string="Niveau de fatigabilité")

    niveau_mob = fields.Boolean(string="Mobilité")

    niveau_vue = fields.Boolean(string="Vue")

    org_ref_recrut = fields.Char(string="Établissement de recrutement")

    patient_ajout = fields.Text(string="Commentaires patient")

    personne_reference_recrut = fields.Char(string="Référence")

    preferences_autre = fields.Text(string="Autres préférences")

    prenom = fields.Char(string="Prénom")

    prob_resp = fields.Boolean(string="Problème respiratoire")

    prob_somm = fields.Boolean(string="Problèmes de sommeil")

    recruteur = fields.Char(string="Responsable de l'entrevue")

    tel_dom_perso = fields.Char(string="No. de téléphone (domicile)")

    tel_mobile_perso = fields.Char(string="No. de cellulaire")

    tel_travail_perso = fields.Char(string="No. de téléphone (travail)")

    test_int_field = fields.Integer(string="test int field")
