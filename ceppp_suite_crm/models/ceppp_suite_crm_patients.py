from odoo import _, api, fields, models


class CepppSuiteCrmPatients(models.Model):
    _name = "ceppp.suite_crm.patients"
    _description = "ceppp_suite_crm_patients"
    _rec_name = "nom"

    nom = fields.Char(string="Nom de famille")

    assistance_audition = fields.Selection(
        selection=[("oui", "Oui"), ("non", "Non")],
        string="Besoin d'assistance",
        help="Avez-vous besoin d'assistance ?",
    )

    assistance_mob = fields.Many2many(
        comodel_name="ceppp.suite_crm.assistance_mob",
        string="Aides à la mobilité",
        help="Veuillez sélectionner toute option qui s'applique",
    )

    assistance_vision = fields.Selection(
        selection=[("oui", "Oui"), ("non", "Non")],
        string="Besoin d'assistance",
        help="Avez-vous besoin d'assistance ?",
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
        help="À quel établissement sera associé le PP ?",
    )

    centre_recrutement = fields.Char(string="Centre de recrutement")

    code_ident = fields.Char(
        string="Code",
        required=True,
    )

    comm_recruteur = fields.Text(
        string="Commentaires recruteur",
        help="Commentaires du recruteur ?",
    )

    comment_refere = fields.Char(
        string="Comment",
        help="Comment avez-vous été référé ?",
    )

    competences_pp = fields.Many2many(
        comodel_name="ceppp.suite_crm.competences_pp",
        string="Compétences",
        help=(
            "Suite à l'entrevue, quelles compétences peuvent être identifiées"
            " chez le PP ?"
        ),
    )

    competences_ppc = fields.Many2many(
        comodel_name="ceppp.suite_crm.competences_ppc",
        string="Compétences",
        help=(
            "Suite à l'entrevue, quelles compétences peuvent être identifiées"
            " chez le PProfilCoach ?"
        ),
    )

    competences_pr = fields.Many2many(
        comodel_name="ceppp.suite_crm.competences_pr",
        string="Compétences",
        help=(
            "Suite à l'entrevue, quelles compétences peuvent être identifiées"
            " chez le PRessource ?"
        ),
    )

    conflit_interet = fields.Selection(
        selection=[("oui", "Oui"), ("non", "Non")],
        string="Conflit d'intérêt",
        help=(
            "En vue du projet sur lequel vous êtes appelé à collaborer comme"
            " patient partenaire, existe-t-il des situations qui pourraient"
            " représenter un conflit d'intérêt réel ou potentiel (ex. membre"
            " d'une association militante, votre employeur, intérêts"
            " financiers personnels, gains pour moi ou un proche par rapport à"
            " un accès à certains soins, engagement idéologique) ?"
        ),
    )

    conflit_interet_detail = fields.Char(
        string="Lequel",
        help="Si oui, lesquels?",
    )

    consentement_dcpp_recrut = fields.Selection(
        selection=[("oui", "Oui"), ("non", "Non")],
        string="Consentement sur l'implication",
        help=(
            "Est-ce que vous consentez à vous impliquer en tant que patient"
            " partenaire ?"
        ),
    )

    consentement_miseajour = fields.Selection(
        selection=[("oui", "Oui"), ("non", "Non")],
        string="Consentement sur la communication",
        help=(
            "Acceptez-vous qu'on communique avec vous annuellement pour des"
            " fins de mise à jour de vos informations?"
        ),
    )

    consentement_recherche = fields.Selection(
        selection=[("oui", "Oui"), ("non", "Non")],
        string="Consentement sur la recherche",
        help=(
            "Acceptez-vous que vos données concernant votre parcours de soins,"
            " vos implications en tant que patients partenaires et vos données"
            " socio démographiques soient utilisées pour des fins de recherche"
            " en lien avec le partenariat ?"
        ),
    )

    consentement_usage_donnees = fields.Selection(
        selection=[("oui", "Oui"), ("non", "Non")],
        string="Consentement sur les données",
        help="Consentez-vous à faire partie de la banque de données ?",
    )

    date_entrevue = fields.Date(
        string="Date de la rencontre téléphonique",
        help="Inscrire la date",
    )

    deplacements = fields.Many2many(
        comodel_name="ceppp.suite_crm.deplacements",
        string="Comment vous déplacez-vous ?",
    )

    descr_exp = fields.Char(
        string="Description de l'expérience",
        help=(
            "Veuillez SVP décrire le type d'impicaiton et le rôle que vous y"
            " avez joué"
        ),
    )

    disponibilites = fields.Many2many(
        comodel_name="ceppp.suite_crm.disponibilites",
        string="Disponibilités",
        help="Quelles sont vos préférences de disponibilité ?",
    )

    domaine_soin_pa = fields.Many2many(
        comodel_name="ceppp.suite_crm.domaine_soin_pa",
        string="Spécialités de soin",
    )

    domaine_soin_pa_2 = fields.Many2many(
        comodel_name="ceppp.suite_crm.domaine_soin_pa",
        string="Spécialité domaine de soins #2",
    )

    domaine_soin_pa_3 = fields.Many2many(
        comodel_name="ceppp.suite_crm.domaine_soin_pa",
        string="Spécialité domaine de soins #3",
    )

    doul_chron = fields.Selection(
        selection=[("oui", "Oui"), ("non", "Non")],
        string="Douleur chronique",
        help="Le pp a-t-il des douleurs chroniques ?",
    )

    duree_experience = fields.Char(
        string="Durée d'expérience (Années / Mois)",
        help=(
            "Au total, depuis combien de temps pensez-vous être impliqué dans"
            " des associations, comités, ou autre ?"
        ),
    )

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
        help="Quel est votre plus haut niveau complété d'éducation",
    )

    education_perso_autre = fields.Char(string="Autre niveau (préciser)")

    email_perso = fields.Char(string="Adresse courriel")

    emploi_perso = fields.Many2many(
        comodel_name="ceppp.suite_crm.emploi_perso",
        string="Emploi du temps",
        help="Quel est votre emploi du temps principal ?",
    )

    etabl_prem_ligne_pa_ = fields.Char(
        string="Établissement de première ligne"
    )

    etabl_sante_pa = fields.Many2one(
        comodel_name="ceppp.suite_crm.hopital",
        string="Établissement de santé principal",
        help=(
            "Dans quel établissement de santé le pp se fait-il principalement"
            " traiter ?"
        ),
    )

    etabl_sante_pa_ = fields.Char(string="Établissement de santé principal")

    etat = fields.Selection(
        selection=[("actif", "Actif"), ("non_actif", "Non-actif")],
        string="État",
    )

    exp_sante = fields.Selection(
        selection=[("oui", "Oui"), ("non", "Non")],
        string="Expérience professionnelle dans le milieu de la santé",
        help="Avez-vous déjà travaillé dans le milieu de santé?",
    )

    exp_sante_detail = fields.Text(
        string="Précisions",
        help=(
            "Si oui, quelle est votre expérience dans le milieu de santé hors"
            " de votre expérience avec la maladie ?"
        ),
    )

    experience_maladie_pa = fields.Text(
        string="Expérience comme pair aidant",
        help="Pouvez-vous décrire votre expérience comme pair aidant ?",
    )

    experience_maladie_pp = fields.Text(
        string="Description de l'expérience",
        help="Pouvez-vous expliquer ?",
    )

    experience_maladie_proche = fields.Text(
        string="Expérience maladie proche",
        help=(
            "Veuillez décrire votre implication dans le parcours de soins de"
            " votre proche"
        ),
    )

    formation_date = fields.Date(
        string="Date de formation",
        help="À quel moment cette formation vous a été donnée ?",
    )

    formation_oui = fields.Char(
        string="Si oui, laquelle",
        help="Quel était le nom de cette formation ?",
    )

    formation_pp = fields.Selection(
        selection=[("oui", "Oui"), ("non", "Non")],
        string="Formation suivie sur le partenariat patient",
        help="Avez-vous déjà suivi une formation sur le partenariat patient ?",
    )

    formation_qui = fields.Char(
        string="Formation par qui",
        help="Par quel organisme a-t-elle été donnée? + où, quand, etc,…",
    )

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

    habiletes_pp = fields.Many2many(
        comodel_name="ceppp.suite_crm.habiletes_pp",
        string="Habiletés",
        help=(
            "Quelles habiletés ou aptitudes personnelles peuvent être"
            " identifiées ?"
        ),
    )

    langue_corresp = fields.Selection(
        selection=[
            ("francais", "Français"),
            ("anglais", "Anglais"),
            ("espagnol", "Espagnol"),
            ("autre", "Autre"),
        ],
        string="Langue de correspondance",
        help="Quelle est votre langue de correspondance préférée",
    )

    langue_parlee = fields.Many2many(
        comodel_name="ceppp.suite_crm.langue_parlee",
        string="Langues parlées",
        help="Quelles langues parlez-vous couramment parmi les suivantes ?",
    )

    membre_assoc_comite = fields.Selection(
        selection=[("oui", "Oui"), ("non", "Non")],
        string="Membre d'une association ou comité",
        help=(
            "Nous aimerions connaître vos implications. Êtes vous membre d'une"
            " association ou d'un comité en lien - ou NON - avec votre"
            " expérience avec la maladie ?"
        ),
    )

    membre_assoc_comite_detail = fields.Char(
        string="Laquelle",
        help="Si oui, laquelle ?",
    )

    motivations_implication = fields.Char(
        string="Motivations à s'impliquer",
        help=(
            "Quelles sont vos motivations à vous impliquer à titre de patient"
            " partenaire au sein de notre organisation ?"
        ),
    )

    naissance_perso = fields.Date(
        string="Date de naissance",
        required=True,
    )

    nas_perso = fields.Integer()

    nas_perso_ = fields.Char(string="Numéro d'assurance social")

    niveau_aud = fields.Selection(
        selection=[("oui", "Oui"), ("non", "Non")],
        string="Ouïe",
        help="Avez-vous des problèmes d'audition ?",
    )

    niveau_autre = fields.Char(
        string="Autres besoins spécifiques",
        help="Précisez d'autres accompagnements dont vous avez besoin",
    )

    niveau_fatigabilite = fields.Selection(
        selection=[("oui", "Oui"), ("non", "Non")],
        string="Niveau de fatigabilité",
        help=(
            "Avez-vous besoin d'accompagnement spécifique au niveau"
            " fatigabilité ?"
        ),
    )

    niveau_mob = fields.Selection(
        selection=[("oui", "Oui"), ("non", "Non")],
        string="Mobilité",
        help=(
            "Avez-vous besoin d'accompagnement spécifique pour la mobilité"
            " réduite ?"
        ),
    )

    niveau_vue = fields.Selection(
        selection=[("oui", "Oui"), ("non", "Non")],
        string="Vue",
        help="Avez-vous des problèmes de la vision ?",
    )

    org_ref_recrut = fields.Char(
        string="Établissement de recrutement",
        help="Quel organisme ?",
    )

    patient_ajout = fields.Text(
        string="Commentaires patient",
        help="Avez-vous d'autres choses à ajouter ?",
    )

    personne_reference_recrut = fields.Char(
        string="Référence",
        help="Qui vous a référé à notre organisation ?",
    )

    preferences = fields.Many2many(
        comodel_name="ceppp.suite_crm.preferences",
        string="Préférences",
        help=(
            "Quelles sont vos disponibilités pour vous impliquer auprès de"
            " notre organisation ?"
        ),
    )

    preferences_autre = fields.Text(
        string="Autres préférences",
        help="Veuillez préciser vos autres intérêts si besoin",
    )

    prenom = fields.Char(string="Prénom")

    prob_resp = fields.Selection(
        selection=[("oui", "Oui"), ("non", "Non")],
        string="Problème respiratoire",
        help="Le pp a-t-il des proiblèmes de respiration ?",
    )

    prob_sant_pa = fields.Many2many(
        comodel_name="ceppp.suite_crm.maladie",
        string="Problématiques de santé",
    )

    prob_sant_pa_2 = fields.Many2one(
        comodel_name="ceppp.suite_crm.maladie",
        string="Problématique de santé #2",
    )

    prob_sant_pa_3 = fields.Many2one(
        comodel_name="ceppp.suite_crm.maladie",
        string="Problématique de santé #3",
    )

    prob_somm = fields.Selection(
        selection=[("oui", "Oui"), ("non", "Non")],
        string="Problèmes de sommeil",
        help="Le pp a-t-il des proiblèmes de sommeil ?",
    )

    recruteur = fields.Char(
        string="Responsable de l'entrevue",
        help="Identifier le recruteur",
    )

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

    role_pp = fields.Many2many(
        comodel_name="ceppp.suite_crm.role_pp",
        string="Role",
        help=(
            "Choisissez les profils de partenaires qui correspondent à vos"
            " activités en lien avec vos implications actuelles de partenariat"
        ),
    )

    tel_dom_perso = fields.Char(string="No. de téléphone (domicile)")

    tel_mobile_perso = fields.Char(string="No. de cellulaire")

    tel_travail_perso = fields.Char(string="No. de téléphone (travail)")

    test_int_field = fields.Integer(string="test int field")
