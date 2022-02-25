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

    conflit_interet = fields.Selection(
        selection=[("oui", "Oui"), ("non", "Non")],
        string="Conflits d'intérêt",
        help=(
            "En vue du projet sur lequel vous êtes appelé à collaborer comme"
            " patient partenaire, existe-t-il des situations qui pourraient"
            " représenter un conflit d'intérêt réel ou potentiel (ex. membre"
            " d'une association militante, votre employeur, intérêts"
            " financiers personnels, gains pour moi ou un proche par rapport à"
            " un accès à certains soins, engagement idéologique) ?"
        ),
    )

    conflit_interet_detail = fields.Text(string="Lesquels")

    descr_exp = fields.Text(
        string="Description de l'expérience",
        help=(
            "Veuillez SVP décrire le type d'impicaiton et le rôle que vous y"
            " avez joué"
        ),
    )

    disponibilites = fields.Many2many(
        comodel_name="ceppp.suite_crm.med_2",
        string="Disponibilités",
        help="Quelles sont vos préférences de disponibilité ?",
    )

    domaine_soin = fields.Many2many(
        comodel_name="ceppp.suite_crm.med_2",
        string="Je suis ou j'ai été suivi(e) dans les spécialités suivantes",
        help=(
            "Veuillez nommer les spécialités pour lesquelles vous avez reçu"
            " des soins"
        ),
    )

    domaine_soin_pa = fields.Many2many(
        comodel_name="ceppp.suite_crm.med_2",
        string="Spécialités de soins",
    )

    duree_experience = fields.Char(
        string="Durée d'expérience (Années / Mois)",
        help=(
            "Au total, depuis combien de temps pensez-vous être impliqué dans"
            " des associations, comités, ou autre ?"
        ),
    )

    etabl_prem_ligne = fields.Many2one(
        comodel_name="ceppp.suite_crm.hopital",
        string="Établissement de première ligne",
        help=(
            "Dans quels établissements de soins et servivces êtes-vous suivis"
            " (ou avez vous été suivis) en première ligne ?"
        ),
    )

    etabl_prem_ligne_pa = fields.Char(string="Établissement de première ligne")

    etabl_sante = fields.Many2one(
        comodel_name="ceppp.suite_crm.hopital",
        string="Établissement de santé principal",
        help=(
            "Dans quels établissements de soins et servivces êtes-vous suivis"
            " (ou avez vous été suivis) ?"
        ),
    )

    etabl_sante_pa = fields.Char(string="Établissement de santé principal")

    exp_decision = fields.Selection(
        selection=[
            ("oui", "Oui"),
            ("non", "Non"),
            ("ne_sait_pas", "Ne sait pas"),
        ],
        string="Expérience prise de décision relative à ses soins médicaux",
        help="Vous sentez-vous partenaires de vos soins ?",
    )

    exp_sante = fields.Selection(
        selection=[("oui", "Oui"), ("non", "Non")],
        string="Expérience professionnelle dans le milieu de la santé",
        help=(
            "Si oui, quelle est votre expérience dans le milieu de santé hors"
            " de votre expérience avec la maladie ?"
        ),
    )

    exp_sante_detail = fields.Text(
        string="Précisions",
        help=(
            "Si oui, quelle est votre expérience dans le milieu de santé hors"
            " de votre expérience avec la maladie ?"
        ),
    )

    experience_maladie = fields.Text(
        string="Expérience maladie",
        help="Veuillez décrire votre problématique de santé",
    )

    experience_maladie_pa = fields.Text(
        string="Expérience comme pair aidant",
        help="Pouvez-vous décrire votre expérience comme pair aidant ?",
    )

    experience_maladie_proche = fields.Text(
        string="Expérience maladie proche",
        help="What is your family member's experience with illness?",
    )

    formation_date = fields.Date(string="Date de formation")

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

    maladie_rare_details = fields.Text(
        string="Maladie rare",
        help="Souffrez-vous d'une maladie rare ? Veuillez la préciser",
    )

    med_1 = fields.Text(
        string="Médicaments",
        help="Prenez-vous des médicaments ? Si oui, lesquels ?",
    )

    med_2 = fields.Many2many(
        comodel_name="ceppp.suite_crm.med_2",
        string="Médicaments #2",
        help="Le pp prend-il des médicaments? Si oui, lesquels ?",
    )

    med_3 = fields.Many2many(
        comodel_name="ceppp.suite_crm.med_2",
        string="Médicaments #3",
        help="Le pp prend-il des médicaments? Si oui, lesquels ?",
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

    membre_assoc_comite_detail = fields.Text(string="Laquelle")

    motivations_implication = fields.Text(
        string="Motivations à s'impliquer",
        help=(
            "Quelles sont vos motivations à vous impliquer à titre de patient"
            " partenaire au sein de notre organisation ?"
        ),
    )

    perspective = fields.Char(help="Quelle est votre perspective ?")

    preferences = fields.Many2many(
        comodel_name="ceppp.suite_crm.med_2",
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

    preneur_decisions = fields.Text(
        string="Preneur de décisions",
        help="Qui prend les décisions qui concernent vos soins et services ?",
    )

    prob_sant = fields.Many2many(
        comodel_name="ceppp.suite_crm.maladie",
        relation="prob_sant_ceppp_suite_crm_perspective_patient_rel",
        string="Problématiques de santé",
        help=(
            "Quel est ou quels sont vos principales problématiques de santé ?"
        ),
    )

    prob_sant_pa = fields.Many2many(
        comodel_name="ceppp.suite_crm.maladie",
        relation="prob_sant_pa_ceppp_suite_crm_perspective_patient_rel",
        string="Problématiques de santé",
    )

    professionnels_sante = fields.Char(string="Professionnels de la santé")

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
        comodel_name="ceppp.suite_crm.med_2",
        string="Rôle",
        help=(
            "Choisissez les profils de partenaires qui correspondent à vos"
            " activités en lien avec vos implications actuelles de partenariat"
        ),
    )
