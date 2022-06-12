from uuid import uuid4

from odoo import _, api, fields, models


class CepppPatient(models.Model):
    _name = "ceppp.patient"
    _description = "ceppp_patient"
    _rec_name = "uuid"

    active = fields.Boolean(
        string="Actif",
        default=True,
        help=(
            "Lorsque non actif, ce patient n'est plus en fonction, mais"
            " demeure accessible."
        ),
    )

    name = fields.Char(
        related="patient_partner_id.name",
    )

    image = fields.Binary(
        related="patient_partner_id.image",
        readonly=True,
    )
    image_medium = fields.Binary(
        related="patient_partner_id.image_medium",
        readonly=True,
    )
    image_small = fields.Binary(
        related="patient_partner_id.image_small",
        readonly=True,
    )

    recruteur_partner_id = fields.Many2one(related="recruteur_user_id.partner_id", string="Recruteur")

    recruteur_user_id = fields.Many2one("res.users", string="Recruteur user")

    centre_recruteur = fields.Char(
        related="patient_partner_id.commercial_company_name",
        string="Centre de recrutement",
        help="Affiliation",
    )

    courriel = fields.Char(
        string="Adresse courriel",
        related="patient_partner_id.email",
    )

    adresse_postale = fields.Char(
        string="Adresse postale",
        related="patient_partner_id.zip",
    )

    telephone = fields.Char(
        string="Téléphone",
        related="patient_partner_id.phone",
    )

    mobile = fields.Char(
        string="Téléphone mobile",
        related="patient_partner_id.mobile",
    )

    uuid = fields.Char(string="Code", help="Identifiant unique anonymisé.")

    date_naissance = fields.Date(
        string="Date de naissance",
        help=(
            "Permet de connaître le groupe d'âge pour des implications"
            " spécifiques."
        ),
    )

    patient_partner_id = fields.Many2one(
        "res.partner",
        string="Patient",
    )

    sexe = fields.Selection(
        selection=[
            ("homme", "Homme"),
            ("femme", "Femme"),
            ("intersexe", "Intersexe"),
            ("null", "Préfère ne pas répondre"),
        ],
        help=(
            "Le sexe fait référence à un ensemble de caractéristiques"
            " biologiques chez les humains et les animaux. Ces"
            " caractéristiques physiques ou physiologiques concernent"
            " principalement les chromosomes, l’expression des gènes, les"
            " niveaux d’hormones et leur fonction, ainsi que l’anatomie de"
            " l’appareil reproducteur. Le sexe comporte habituellement deux"
            " catégories (mâle, femelle); cependant, les caractéristiques"
            " biologiques liées au sexe et l’expression de ces"
            " caractéristiques peuvent varier."
        ),
    )

    genre = fields.Selection(
        selection=[
            ("homme", "Homme"),
            ("femme", "Femme"),
            ("bispirituelle", "Bispirituel.le"),
            ("autre", "Autre"),
        ],
        help=(
            "Le genre fait référence aux rôles, aux comportements, aux"
            " expressions et aux identités des filles, des femmes, des"
            " garçons, des hommes et des personnes de diverses identités de"
            " genre. Le genre influence la perception que les individus ont"
            " d'eux-mêmes ou d'autrui, leur manière d'agir ou d'interagir,"
            " ainsi que la répartition du pouvoir et des ressources dans la"
            " société. Bien que le genre soit habituellement conceptualisé en"
            " termes binaires (fille/femme et garçon/homme), les individus et"
            " les groupes comprennent, expérimentent et expriment leur genre"
            " de diverses façons."
        ),
    )

    genre_autre = fields.Char(
        string="Autre genre",
        help="Peut être défini lorsque le genre est au choix 'autre'.",
    )

    occupation = fields.Selection(
        selection=[
            ("travailleur", "Travailleur.se"),
            ("retraite", "Retraité.e"),
            ("benevole", "Bénévole"),
            ("etudiant", "Étudiant.e"),
            ("proche_aidant", "Proche aidant.e"),
            ("parent_maison", "Parent à la maison"),
            ("autre", "Autre"),
        ],
        help="Occupation principale du temps",
    )

    occupation_autre = fields.Char(
        string="Autre occupation",
        help="Peut être défini lorsque l'occupation est au choix 'autre'.",
    )

    formation_professionnelle = fields.Char(
        string="Formation professionnelle",
        help="Plus haut diplôme obtenu et domaine",
    )

    heritage_culturel = fields.Selection(
        string="Héritage culturel",
        selection=[
            ("oui", "Oui"),
            ("non", "Non"),
            ("ne_pas_repondre", "Préfère ne pas répondre"),
        ],
        help=(
            "Est-ce que vous vous identifiez comme membre d'une minorité"
            " visible, au sens de la Loi sur l'équité en matière d'emploi."
            " Selon cette loi, les personnes, autres que les Premiers Peuples,"
            " qui ne sont pas caucasiens ou qui n'ont pas la peau blanche font"
            " partie des minorités visibles. À cela s'ajoute également"
            " l'héritage culturel associées aux minorités visibles comme les"
            " pratiques, représentations, expressions, connaissances et"
            " savoir-faire - ainsi que les instruments, objets, artefacts et"
            " espaces culturels qui leur sont associés - que les communautés,"
            " les groupes et, le cas échéant, les individus reconnaissent"
            " comme faisant partie de leur patrimoine culturel. Ce patrimoine"
            " culturel immatériel, transmis de génération en génération, est"
            " recréé en permanence par les communautés et groupes en fonction"
            " de leur milieu, de leur interaction avec la nature et de leur"
            " histoire, et leur procure un sentiment d’identité et de"
            " continuité, contribuant ainsi à promouvoir le respect de la"
            " diversité culturelle et la créativité humaine (Référence:"
            " https://ich.unesco.org/fr/convention#art2)."
        ),
    )

    langue_parle_ecrit = fields.Many2many(
        comodel_name="ceppp.langue",
        string="Langues parlées/écrites",
    )

    langue_parle_ecrit_autre = fields.Char(
        string="Autre langues parlées/écrites",
        help=(
            "Peut être défini lorsque la langue parlées/écrites est au choix"
            " 'autre'."
        ),
    )

    mode_communication_privilegie = fields.Selection(
        string="Mode de communication privilégié",
        selection=[
            ("telephone", "Téléphone"),
            ("courriel", "Courriel"),
        ],
    )

    patient_actif = fields.Selection(
        string="Patient actif-passif",
        selection=[
            ("actif", "Actif"),
            ("passif", "Passif"),
        ],
        help=(
            "Actif: patient partenaire est disponible à participer dans des"
            " projets. Passif: patient partenaire n'est pas disponible à"
            " participer dans des projets."
        ),
    )

    competence_patient = fields.Selection(
        string="Compétences au partenariat",
        selection=[
            ("1", "Se connaître dans la vie avec la maladie"),
            ("2", "Redonner un sens à sa vie au travers de ses expériences"),
            ("3", "Mobiliser ses savoirs expérientiels"),
            ("4", "Développer sa résilience"),
            ("5", "Faire preuve d’altruisme"),
            ("6", "Être réflexif et transmettre"),
            ("7", "Être à l'écoute"),
            ("8", "Se raconter de façon pédagogique"),
            ("9", "communiquer"),
        ],
        help="Compétences du patient.",
    )

    commentaires = fields.Text(
        string="Commentaires",
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if "uuid" not in vals.keys():
                vals["uuid"] = str(uuid4())
        return super(CepppPatient, self).create(vals_list)
