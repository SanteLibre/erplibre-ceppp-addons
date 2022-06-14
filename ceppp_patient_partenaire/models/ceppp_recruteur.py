from uuid import uuid4

from odoo import _, api, fields, models


class CepppRecruteur(models.Model):
    _name = "ceppp.recruteur"
    _inherit = ["mail.activity.mixin", "mail.thread"]
    _description = "ceppp_recruteur"

    name = fields.Char(
        related="patient_partner_id.name",
        track_visibility="onchange",
    )

    active = fields.Boolean(
        string="Actif",
        track_visibility="onchange",
        default=True,
        help=(
            "Lorsque non actif, ce patient n'est plus en fonction, mais"
            " demeure accessible."
        ),
    )

    disponibilite = fields.Many2many(
        comodel_name="ceppp.disponibilite",
        string="Disponible",
        track_visibility="onchange",
        help="Jour de la semaine de disponible",
    )

    disponibilite_not = fields.Many2many(
        comodel_name="ceppp.disponibilite",
        string="Non disponible",
        track_visibility="onchange",
        relation="ceppp_recruteur_disponibilite_not_rel",
        help="Jour de la semaine de non-disponible",
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

    recruteur_partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Recruteur",
        track_visibility="onchange",
    )

    recruteur_user_id = fields.Many2one(
        comodel_name="res.users",
        string="Recruteur user",
        compute="_compute_recruteur_user_id",
        store=True,
    )

    consentement_notification = fields.Boolean(
        string="Consentement aux notifications/communications",
        track_visibility="onchange",
    )

    consentement_recrutement = fields.Boolean(
        string="Consentement au recrutement",
        track_visibility="onchange",
        help=(
            "Consentement dans le cadre d'activités de partenariat. Si vous"
            " voulez vous retirer en tant que patient partenaire, veuillez"
            " envoyer un courriel à cette adresse <mail - formulaire"
            " prérempli?>"
        ),
    )

    consentement_recherche = fields.Boolean(
        string="Consentement à la recherche",
        track_visibility="onchange",
        help=(
            "Consentement dans le cadre d'activités de recherche sur le"
            " partenariat."
        ),
    )

    centre_recruteur = fields.Char(
        related="patient_partner_id.parent_id.name",
        string="Centre de recrutement",
        track_visibility="onchange",
        help="Affiliation",
    )

    courriel = fields.Char(
        string="Adresse courriel",
        track_visibility="onchange",
        related="patient_partner_id.email",
    )

    adresse_postale = fields.Char(
        string="Adresse postale",
        track_visibility="onchange",
        related="patient_partner_id.zip",
    )

    telephone = fields.Char(
        string="Téléphone",
        track_visibility="onchange",
        related="patient_partner_id.phone",
    )

    mobile = fields.Char(
        string="Téléphone mobile",
        track_visibility="onchange",
        related="patient_partner_id.mobile",
    )

    uuid = fields.Char(
        string="Code",
        track_visibility="onchange",
        help="Identifiant unique anonymisé.",
    )

    date_naissance = fields.Date(
        string="Date de naissance",
        track_visibility="onchange",
        help=(
            "Permet de connaître le groupe d'âge pour des implications"
            " spécifiques."
        ),
    )

    patient_partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Patient",
        track_visibility="onchange",
    )

    sexe = fields.Selection(
        selection=[
            ("homme", "Homme"),
            ("femme", "Femme"),
            ("intersexe", "Intersexe"),
            ("null", "Préfère ne pas répondre"),
        ],
        track_visibility="onchange",
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
        track_visibility="onchange",
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
        track_visibility="onchange",
        help="Peut être défini lorsque le genre est au choix 'autre'.",
    )

    occupation = fields.Many2many(
        comodel_name="ceppp.occupation",
        track_visibility="onchange",
        help="Occupation principale du temps",
    )

    occupation_autre = fields.Char(
        string="Autre occupation",
        track_visibility="onchange",
        help="Peut être défini lorsque l'occupation est au choix 'autre'.",
    )

    formation_professionnelle = fields.Char(
        string="Formation professionnelle",
        track_visibility="onchange",
        help="Plus haut diplôme obtenu et domaine",
    )

    heritage_culturel = fields.Selection(
        selection=[
            ("oui", "Oui"),
            ("non", "Non"),
            ("ne_pas_repondre", "Préfère ne pas répondre"),
        ],
        string="Héritage culturel",
        track_visibility="onchange",
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
        track_visibility="onchange",
    )

    langue_parle_ecrit_autre = fields.Char(
        string="Autre langues parlées/écrites",
        track_visibility="onchange",
        help=(
            "Peut être défini lorsque la langue parlées/écrites est au choix"
            " 'autre'."
        ),
    )

    mode_communication_privilegie = fields.Many2many(
        comodel_name="ceppp.mode_communication_privilegie",
        string="Mode de communication privilégié",
        track_visibility="onchange",
    )

    maladie_soi_meme = fields.Many2many(
        comodel_name="ceppp.maladie",
        string="Problématiques de santé (soi-même)",
        track_visibility="onchange",
    )

    maladie_proche_aidant = fields.One2many(
        comodel_name="ceppp.maladie_proche_aidant",
        inverse_name="recruteur_id",
        string=(
            "Problématiques de santé de la personne accompagnée (vous en tant"
            " que proche-aidant)"
        ),
        track_visibility="onchange",
    )

    formation = fields.One2many(
        comodel_name="ceppp.formation",
        inverse_name="recruteur_id",
        track_visibility="onchange",
    )

    implication = fields.One2many(
        comodel_name="ceppp.implication",
        inverse_name="recruteur_id",
        track_visibility="onchange",
    )

    patient_actif = fields.Selection(
        selection=[("actif", "Actif"), ("passif", "Passif")],
        string="Patient actif-passif",
        track_visibility="onchange",
        help=(
            "Actif: patient partenaire est disponible à participer dans des"
            " projets. Passif: patient partenaire n'est pas disponible à"
            " participer dans des projets."
        ),
    )

    competence_patient = fields.Many2many(
        comodel_name="ceppp.competence",
        string="Compétences au partenariat",
        track_visibility="onchange",
        help="Compétences du patient.",
    )

    commentaires = fields.Text(
        string="Commnentaires",
        track_visibility="onchange",
    )

    user_is_admin = fields.Boolean(
        store=False,
        compute="_compute_user_is_admin",
    )

    occupation_is_autre = fields.Boolean(
        compute="_compute_occupation_is_autre"
    )

    langue_is_autre = fields.Boolean(compute="_compute_langue_is_autre")

    @api.depends("occupation")
    def _compute_occupation_is_autre(self):
        for record in self:
            record.occupation_is_autre = (
                self.env.ref("ceppp_patient_partenaire.ceppp_occupation_7").id
                in record.occupation.ids
            )

    @api.depends("langue_parle_ecrit")
    def _compute_langue_is_autre(self):
        for record in self:
            record.langue_is_autre = (
                self.env.ref("ceppp_patient_partenaire.ceppp_langue_autre").id
                in record.langue_parle_ecrit.ids
            )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if "uuid" not in vals.keys():
                vals["uuid"] = str(uuid4())
        return super(CepppRecruteur, self).create(vals_list)

    @api.depends("recruteur_partner_id")
    def _compute_recruteur_user_id(self):
        for record in self:
            if (
                record.recruteur_partner_id
                and record.recruteur_partner_id.user_ids
            ):
                record.recruteur_user_id = (
                    record.recruteur_partner_id.user_ids[0].id
                )
            else:
                record.recruteur_user_id = False

    @api.depends("patient_partner_id")
    def _compute_user_is_admin(self):
        for record in self:
            record.user_is_admin = (
                self.env["res.users"].browse(self._uid).partner_id.ceppp_entity
                == "administrateur"
            )
