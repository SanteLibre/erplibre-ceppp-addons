from odoo import _, api, fields, models


class CepppSuiteCrmPatients(models.Model):
    _name = "ceppp.suite_crm.patients"
    _description = "ceppp_suite_crm_patients"
    _rec_name = "nom"

    nom = fields.Char(string="Nom de famille")

    assistance_audition = fields.Selection(
        selection=[("oui", "Oui"), ("non", "Non")],
        string="Besoin d'assistance",
    )

    assistance_mob = fields.Selection(
        selection=[
            ("fauteuil_roulant", "Fauteuil roulant"),
            ("canne", "Canne"),
            ("transport_adapte", "Transport adapté"),
        ],
        string="Aides à la mobilité",
    )

    assistance_vision = fields.Selection(
        selection=[("oui", "Oui"), ("non", "Non")],
        string="Besoin d'assistance",
    )

    association_etablissement_recr = fields.Selection(
        selection=[
            ("ceppp", "CEPPP"),
            ("dcpp", "DCPP"),
            ("inesss", "INESSS"),
            ("ruis_u_de_l", "RUIS UdeL"),
            ("ruis_u_de_s", "RUIS UdeS"),
            ("ruis_u_de_m", "RUIS UdeM"),
            ("ruis_mcgill", "RUIS McGill"),
            ("reseau1", "Réseau-1"),
            ("chum", "CHUM"),
            ("canvector", "CanVector"),
            ("canet", "CANet"),
        ],
        string="Établissement de recrutement",
    )

    centre_recrutement = fields.Char(string="Centre de recrutement")

    code_ident = fields.Char(
        string="Code",
        required=True,
    )

    comm_recruteur = fields.Text(string="Commentaires recruteur")

    comment_refere = fields.Char(string="Comment")

    competences_pp = fields.Selection(
        selection=[
            (
                "se_connait_dans_la_vie_avec_la_maladie",
                "Se connaît dans la vie avec la maladie",
            ),
            (
                "mobilise_ses_savoirs_experientiels",
                "Mobilise ses savoirs expérientiels",
            ),
            ("developpe_sa_resilience", "Développe sa résilience"),
            (
                "redonne_un_sens_a_la_vie_au_travers_de_ses_experiences",
                "Redonne un sens à la vie au travers de ses expériences",
            ),
            (
                "elabore_un_projet_de_vie_et_l_adapte_au_changement",
                "Élabore un projet de vie et l'adapte au changement",
            ),
            ("fait_preuve_d_altruisme", "Fait preuve d'altruisme"),
            (
                "se_raconte_de_facon_pedagogique",
                "Se racconte de façon pédagogique",
            ),
            ("communique", "Communique"),
            ("est_reflexif_et_transmet", "Est réflexif et transmet"),
            ("est_a_l_ecoute", "Est à l'écoute"),
            (
                "mobilise_ses_experiences_sociales_et_professionnelles",
                "Mobilise ses expériences sociales et professionnelles",
            ),
            ("assume_un_co_leadership", "Assume un co-leadership"),
            (
                "accompagne_un_individu_ou_un_groupe",
                "Accompagne un individu ou un groupe",
            ),
            (
                "analyse_des_situations_relationelles_de_differents_niveaux_de_complexite",
                "Analyse des situations relationelles de différents niveaux de"
                " complexité",
            ),
            (
                "tisse_et_entretien_des_reseaux",
                "Tisse et entretien des réseaux",
            ),
            ("s_exprime_clairement", "S'exprime clairement"),
            (
                "habiletes_interpersonnelles",
                "Habiletés interpersonnelles (écoute, empathie)",
            ),
            (
                "desir_d_aider_autrui_et_de_contribuer_a_un_objectif_qui_depasse_sa_propre_situation",
                "Désir d'aider autrui et de contribuer à un objectif qui"
                " dépasse sa propre situation",
            ),
            (
                "Manifeste_un_desir_d_implication",
                "Manifeste un désir d'implication (associations, benevolat,"
                " temoignages)",
            ),
        ],
        string="Compétences",
    )

    competences_ppc = fields.Selection(
        selection=[
            (
                "mobilise_ses_experiences_sociales_et_professionnelles",
                "Mobilise ses expériences sociales et professionnelles",
            ),
            ("assume_un_co_leadership", "Assume un co-leadership"),
            (
                "accompagne_un_individu_ou_un_groupe",
                "Accompagne un individu ou un groupe",
            ),
            (
                "analyse_des_situations_relationelles_de_differents_niveaux_de_complexite",
                "Analyse des situations relationelles de différents niveaux de"
                " complexité",
            ),
            (
                "tisse_et_entretien_des_reseaux",
                "Tisse et entretien des réseaux",
            ),
        ],
        string="Compétences",
    )

    competences_pr = fields.Selection(
        selection=[
            ("fait_preuve_d_altruisme", "Fait preuve d'altruisme"),
            (
                "se_raconte_de_facon_pedagogique",
                "Se racconte de façon pédagogique",
            ),
            ("communique", "Communique"),
            ("est_reflexif_et_transmet", "Est réflexif et transmet"),
            ("est_a_l_ecoute", "Est à l'écoute"),
        ],
        string="Compétences",
    )

    conflit_interet = fields.Selection(
        selection=[("oui", "Oui"), ("non", "Non")],
        string="Conflit d'intérêt",
    )

    conflit_interet_detail = fields.Char(string="Lequel")

    consentement_dcpp_recrut = fields.Selection(
        selection=[("oui", "Oui"), ("non", "Non")],
        string="Consentement sur l'implication",
    )

    consentement_miseajour = fields.Selection(
        selection=[("oui", "Oui"), ("non", "Non")],
        string="Consentement sur la communication",
    )

    consentement_recherche = fields.Selection(
        selection=[("oui", "Oui"), ("non", "Non")],
        string="Consentement sur la recherche",
    )

    consentement_usage_donnees = fields.Selection(
        selection=[("oui", "Oui"), ("non", "Non")],
        string="Consentement sur les données",
    )

    date_entrevue = fields.Date(string="Date de la rencontre téléphonique")

    deplacements = fields.Selection(
        selection=[
            ("voiture", "En voiture"),
            ("transport_adapte", "En transport adapté"),
            ("autre", "Autrement"),
        ],
        string="Comment vous déplacez-vous ?",
    )

    descr_exp = fields.Char(string="Description de l'expérience")

    disponibilites = fields.Selection(
        selection=[
            ("matin", "Matin"),
            ("apresmidi", "Après-midi"),
            ("soir", "Soir"),
            ("fins_de_semaine", "Fins de semaine"),
            ("jours", "Jours"),
        ],
        string="Disponibilités",
    )

    domaine_soin_pa = fields.Selection(
        selection=[
            ("allergologie_ou_l_immunologie", "Allergologie ou l'immunologie"),
            ("anesthesiologie", "Anesthésiologie"),
            ("andrologie", "Andrologie"),
            ("cardiologie", "Cardiologie"),
            ("chirurgie_cardiaque", "Chirurgie cardiaque"),
            (
                "chirurgie_esthetique_plastique_et_reconstructive",
                "Chirurgie esthétique plastique et reconstructive",
            ),
            ("chirurgie_generale", "Chirurgie générale"),
            ("chirurgie_maxillo_faciale", "Chirurgie maxillo-faciale"),
            ("chirurgie_pediatrique", "Chirurgie pédiatrique"),
            ("chirurgie_thoracique", "Chirurgie thoracique"),
            ("chirurgie_vasculaire", "Chirurgie vasculaire"),
            ("neurochirurgie", "Neurochirurgie"),
            ("dermatologie", "Dermatologie"),
            ("endocrinologie", "Endocrinologie"),
            ("gastro_enterologie", "Gastro-entérologie"),
            ("geriatrie", "Gériatrie"),
            ("gynecologie", "Gynécologie"),
            ("hematologie", "Hématologie"),
            ("hepatologie", "Hépatologie"),
            ("infectiologie", "Infectiologie"),
            ("medecine_aigue", "Médecine aiguë"),
            ("medecine_du_travail", "Médecine du travail"),
            ("medecine_generale", "Médecine générale"),
            ("medecine_interne", "Médecine interne"),
            ("medecine_nucleaire", "Médecine nucléaire"),
            ("medecine_palliative", "Médecine palliative"),
            ("medecine_physique", "Médecine physique"),
            ("medecine_preventive", "Médecine préventive"),
            ("neonatologie", "Néonatologie"),
            ("nephrologie", "Néphrologie"),
            ("neurologie", "Neurologie"),
            ("odontologie", "Odontologie"),
            ("oncologie", "Oncologie"),
            ("obstetrique", "Obstétrique"),
            ("ophtalmologie", "Ophtalmologie"),
            ("orthopedie", "Orthopédie"),
            ("oto_rhino_laryngologie", "Oto-rhino-laryngologie"),
            ("pediatrie", "Pédiatrie"),
            ("pneumologie", "Pneumologie"),
            ("psychiatrie", "Psychiatrie"),
            ("radiologie", "Radiologie"),
            ("radiotherapie", "Radiothérapie"),
            ("rhumatologie", "Rhumatologie"),
            ("urologie", "Urologie"),
        ],
        string="Spécialités de soin",
    )

    domaine_soin_pa_2 = fields.Selection(
        selection=[
            ("allergologie_ou_l_immunologie", "Allergologie ou l'immunologie"),
            ("anesthesiologie", "Anesthésiologie"),
            ("andrologie", "Andrologie"),
            ("cardiologie", "Cardiologie"),
            ("chirurgie_cardiaque", "Chirurgie cardiaque"),
            (
                "chirurgie_esthetique_plastique_et_reconstructive",
                "Chirurgie esthétique plastique et reconstructive",
            ),
            ("chirurgie_generale", "Chirurgie générale"),
            ("chirurgie_maxillo_faciale", "Chirurgie maxillo-faciale"),
            ("chirurgie_pediatrique", "Chirurgie pédiatrique"),
            ("chirurgie_thoracique", "Chirurgie thoracique"),
            ("chirurgie_vasculaire", "Chirurgie vasculaire"),
            ("neurochirurgie", "Neurochirurgie"),
            ("dermatologie", "Dermatologie"),
            ("endocrinologie", "Endocrinologie"),
            ("gastro_enterologie", "Gastro-entérologie"),
            ("geriatrie", "Gériatrie"),
            ("gynecologie", "Gynécologie"),
            ("hematologie", "Hématologie"),
            ("hepatologie", "Hépatologie"),
            ("infectiologie", "Infectiologie"),
            ("medecine_aigue", "Médecine aiguë"),
            ("medecine_du_travail", "Médecine du travail"),
            ("medecine_generale", "Médecine générale"),
            ("medecine_interne", "Médecine interne"),
            ("medecine_nucleaire", "Médecine nucléaire"),
            ("medecine_palliative", "Médecine palliative"),
            ("medecine_physique", "Médecine physique"),
            ("medecine_preventive", "Médecine préventive"),
            ("neonatologie", "Néonatologie"),
            ("nephrologie", "Néphrologie"),
            ("neurologie", "Neurologie"),
            ("odontologie", "Odontologie"),
            ("oncologie", "Oncologie"),
            ("obstetrique", "Obstétrique"),
            ("ophtalmologie", "Ophtalmologie"),
            ("orthopedie", "Orthopédie"),
            ("oto_rhino_laryngologie", "Oto-rhino-laryngologie"),
            ("pediatrie", "Pédiatrie"),
            ("pneumologie", "Pneumologie"),
            ("psychiatrie", "Psychiatrie"),
            ("radiologie", "Radiologie"),
            ("radiotherapie", "Radiothérapie"),
            ("rhumatologie", "Rhumatologie"),
            ("urologie", "Urologie"),
        ],
        string="Spécialité domaine de soins #2",
    )

    domaine_soin_pa_3 = fields.Selection(
        selection=[
            ("allergologie_ou_l_immunologie", "Allergologie ou l'immunologie"),
            ("anesthesiologie", "Anesthésiologie"),
            ("andrologie", "Andrologie"),
            ("cardiologie", "Cardiologie"),
            ("chirurgie_cardiaque", "Chirurgie cardiaque"),
            (
                "chirurgie_esthetique_plastique_et_reconstructive",
                "Chirurgie esthétique plastique et reconstructive",
            ),
            ("chirurgie_generale", "Chirurgie générale"),
            ("chirurgie_maxillo_faciale", "Chirurgie maxillo-faciale"),
            ("chirurgie_pediatrique", "Chirurgie pédiatrique"),
            ("chirurgie_thoracique", "Chirurgie thoracique"),
            ("chirurgie_vasculaire", "Chirurgie vasculaire"),
            ("neurochirurgie", "Neurochirurgie"),
            ("dermatologie", "Dermatologie"),
            ("endocrinologie", "Endocrinologie"),
            ("gastro_enterologie", "Gastro-entérologie"),
            ("geriatrie", "Gériatrie"),
            ("gynecologie", "Gynécologie"),
            ("hematologie", "Hématologie"),
            ("hepatologie", "Hépatologie"),
            ("infectiologie", "Infectiologie"),
            ("medecine_aigue", "Médecine aiguë"),
            ("medecine_du_travail", "Médecine du travail"),
            ("medecine_generale", "Médecine générale"),
            ("medecine_interne", "Médecine interne"),
            ("medecine_nucleaire", "Médecine nucléaire"),
            ("medecine_palliative", "Médecine palliative"),
            ("medecine_physique", "Médecine physique"),
            ("medecine_preventive", "Médecine préventive"),
            ("neonatologie", "Néonatologie"),
            ("nephrologie", "Néphrologie"),
            ("neurologie", "Neurologie"),
            ("odontologie", "Odontologie"),
            ("oncologie", "Oncologie"),
            ("obstetrique", "Obstétrique"),
            ("ophtalmologie", "Ophtalmologie"),
            ("orthopedie", "Orthopédie"),
            ("oto_rhino_laryngologie", "Oto-rhino-laryngologie"),
            ("pediatrie", "Pédiatrie"),
            ("pneumologie", "Pneumologie"),
            ("psychiatrie", "Psychiatrie"),
            ("radiologie", "Radiologie"),
            ("radiotherapie", "Radiothérapie"),
            ("rhumatologie", "Rhumatologie"),
            ("urologie", "Urologie"),
        ],
        string="Spécialité domaine de soins #3",
    )

    doul_chron = fields.Selection(
        selection=[("oui", "Oui"), ("non", "Non")],
        string="Douleur chronique",
    )

    duree_experience = fields.Char(string="Durée d'expérience (Années / Mois)")

    education_perso = fields.Selection(
        selection=[
            ("primaire", "Primaire"),
            ("secondaire", "Secondaire"),
            ("formation_professionnelle", "Formation professionnelle"),
            ("post_secondaire", "Post-secondaire"),
            ("maitrise", "MaÎtrise"),
            ("doctorat", "Doctorat"),
            ("certificat", "Certificat"),
            ("autre", "Autre"),
        ],
        string="Formation professionnelle",
    )

    education_perso_autre = fields.Char(string="Autre niveau (préciser)")

    email_perso = fields.Char(string="Adresse courriel")

    emploi_perso = fields.Selection(
        selection=[
            ("emploi", "Emploi"),
            ("benevolat", "Bénévolat"),
            ("famille", "Famille"),
            ("proche", "Proche"),
            ("autre", "Autre"),
        ],
        string="Emploi du temps",
    )

    etabl_prem_ligne_pa_ = fields.Char(
        string="Établissement de première ligne"
    )

    etabl_sante_pa_ = fields.Char(string="Établissement de santé principal")

    etat = fields.Selection(
        selection=[("actif", "Actif"), ("non_actif", "Non-actif")],
        string="État",
    )

    exp_sante = fields.Selection(
        selection=[("oui", "Oui"), ("non", "Non")],
        string="Expérience professionnelle dans le milieu de la santé",
    )

    exp_sante_detail = fields.Text(string="Précisions")

    experience_maladie_pa = fields.Text(string="Expérience comme pair aidant")

    experience_maladie_pp = fields.Text(string="Description de l'expérience")

    experience_maladie_proche = fields.Text(string="Expérience maladie proche")

    formation_date = fields.Date(string="Date de formation")

    formation_oui = fields.Char(string="Si oui, laquelle")

    formation_pp = fields.Selection(
        selection=[("oui", "Oui"), ("non", "Non")],
        string="Formation suivie sur le partenariat patient",
    )

    formation_qui = fields.Char(string="Formation par qui")

    genre = fields.Selection(
        selection=[("homme", "Homme"), ("femme", "Femme"), ("autre", "Autre")],
        required=True,
    )

    groupe_designe = fields.Selection(
        selection=[
            ("blanc", "Blanc"),
            ("noir", "Noir"),
            ("afro_americain", "Afro-Américain"),
            ("premiere_nation", "Première nation"),
            ("asiatique", "Asiatique"),
        ],
        string="Origine ethnique ou culturelle",
    )

    habiletes_pp = fields.Selection(
        selection=[
            ("s_exprime_clairement", "S'exprime clairement"),
            (
                "habiletes_interpersonnelles",
                "Habiletés interpersonnelles (écoute, empathie)",
            ),
            (
                "desir_d_aider_autrui_et_de_contribuer_a_un_objectif_qui_depasse_sa_propre_situation",
                "Désir d'aider autrui et de contribuer à un objectif qui"
                " dépasse sa propre situation",
            ),
            (
                "Manifeste_un_desir_d_implication",
                "Manifeste un désir d'implication (associations, benevolat,"
                " temoignages)",
            ),
        ],
        string="Habiletés",
    )

    langue_corresp = fields.Selection(
        selection=[
            ("francais", "Français"),
            ("anglais", "Anglais"),
            ("espagnol", "Espagnol"),
            ("autre", "Autre"),
        ],
        string="Langue de correspondance",
    )

    langue_parlee = fields.Selection(
        selection=[
            ("francais", "Français"),
            ("anglais", "Anglais"),
            ("espagnol", "Espagnol"),
            ("autre", "Autre"),
        ],
        string="Langues parlées",
    )

    membre_assoc_comite = fields.Selection(
        selection=[("oui", "Oui"), ("non", "Non")],
        string="Membre d'une association ou comité",
    )

    membre_assoc_comite_detail = fields.Char(string="Laquelle")

    motivations_implication = fields.Char(string="Motivations à s'impliquer")

    naissance_perso = fields.Date(
        string="Date de naissance",
        required=True,
    )

    nas_perso = fields.Integer()

    nas_perso_ = fields.Char(string="Numéro d'assurance social")

    niveau_aud = fields.Selection(
        selection=[("oui", "Oui"), ("non", "Non")],
        string="Ouïe",
    )

    niveau_autre = fields.Char(string="Autres besoins spécifiques")

    niveau_fatigabilite = fields.Selection(
        selection=[("oui", "Oui"), ("non", "Non")],
        string="Niveau de fatigabilité",
    )

    niveau_mob = fields.Selection(
        selection=[("oui", "Oui"), ("non", "Non")],
        string="Mobilité",
    )

    niveau_vue = fields.Selection(
        selection=[("oui", "Oui"), ("non", "Non")],
        string="Vue",
    )

    org_ref_recrut = fields.Char(string="Établissement de recrutement")

    patient_ajout = fields.Text(string="Commentaires patient")

    personne_reference_recrut = fields.Char(string="Référence")

    preferences = fields.Selection(
        selection=[
            ("recherche", "Recherche"),
            ("gouvernance", "Gouvernance"),
            ("tables_travail", "Tables de travail"),
            ("comites", "Comités"),
            ("milieux_soins", "Milieux de soins"),
            ("enseignement", "Enseignement"),
            ("interets_autre", "Autre"),
        ],
        string="Préférences",
    )

    preferences_autre = fields.Text(string="Autres préférences")

    prenom = fields.Char(string="Prénom")

    prob_resp = fields.Selection(
        selection=[("oui", "Oui"), ("non", "Non")],
        string="Problème respiratoire",
    )

    prob_somm = fields.Selection(
        selection=[("oui", "Oui"), ("non", "Non")],
        string="Problèmes de sommeil",
    )

    recruteur = fields.Char(string="Responsable de l'entrevue")

    rel_patient = fields.Selection(
        selection=[
            ("parent", "Parent"),
            ("enfant", "Enfant"),
            ("conjoint", "Conjoint(e)"),
            ("famille_elargie", "Famille élargie"),
            ("autre", "Autre"),
        ],
        string="Relation avec le patient",
    )

    role_pp = fields.Selection(
        selection=[
            ("coach", "Coach"),
            ("co_chercheur", "Co-chercheur"),
            ("formateur", "Formateur"),
            ("accompagnateur", "Accompagnateur"),
            ("aviseur", "Aviseur"),
        ],
        string="Role",
    )

    tel_dom_perso = fields.Char(string="No. de téléphone (domicile)")

    tel_mobile_perso = fields.Char(string="No. de cellulaire")

    tel_travail_perso = fields.Char(string="No. de téléphone (travail)")

    test_int_field = fields.Integer(string="test int field")
