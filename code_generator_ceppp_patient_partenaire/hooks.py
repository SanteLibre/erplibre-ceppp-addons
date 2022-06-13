import logging
import os

from odoo import SUPERUSER_ID, _, api, fields, models

_logger = logging.getLogger(__name__)

MODULE_NAME = "ceppp_patient_partenaire"


def post_init_hook(cr, e):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})

        # The path of the actual file
        path_module_generate = os.path.normpath(
            os.path.join(os.path.dirname(__file__), "..")
        )

        short_name = MODULE_NAME.replace("_", " ").title()

        # Add code generator
        categ_id = env["ir.module.category"].search(
            [("name", "=", "Uncategorized")], limit=1
        )
        value = {
            "shortdesc": short_name,
            "name": MODULE_NAME,
            "license": "AGPL-3",
            "category_id": categ_id.id,
            "summary": "",
            "author": "SantéLibre",
            "website": "https://santelibre.ca",
            "application": True,
            "enable_sync_code": True,
            "path_sync_code": path_module_generate,
            "icon": os.path.join(
                os.path.dirname(__file__),
                "static",
                "description",
                "code_generator_icon.png",
            ),
        }

        # TODO HUMAN: enable your functionality to generate
        value["enable_sync_template"] = True
        value["ignore_fields"] = ""
        value["post_init_hook_show"] = False
        value["uninstall_hook_show"] = False
        value["post_init_hook_feature_code_generator"] = False
        value["uninstall_hook_feature_code_generator"] = False

        value["hook_constant_code"] = f'MODULE_NAME = "{MODULE_NAME}"'

        code_generator_id = env["code.generator.module"].create(value)

        # Add dependencies
        lst_depend_module = ["contacts", "mail"]
        code_generator_id.add_module_dependency(lst_depend_module)

        # Add/Update Ceppp Chapitre Maladie
        model_model = "ceppp.chapitre_maladie"
        model_name = "ceppp_chapitre_maladie"
        dct_model = {
            "description": "ceppp_chapitre_maladie",
            "rec_name": "nom",
        }
        dct_field = {
            "nom": {
                "code_generator_form_simple_view_sequence": 10,
                "code_generator_sequence": 3,
                "code_generator_tree_view_sequence": 10,
                "field_description": "Nom",
                "ttype": "char",
            },
        }
        model_ceppp_chapitre_maladie = code_generator_id.add_update_model(
            model_model,
            model_name,
            dct_field=dct_field,
            dct_model=dct_model,
        )

        # Add/Update Ceppp Competence
        model_model = "ceppp.competence"
        model_name = "ceppp_competence"
        dct_model = {
            "description": "ceppp_competence",
        }
        dct_field = {
            "name": {
                "code_generator_form_simple_view_sequence": 10,
                "code_generator_sequence": 2,
                "code_generator_tree_view_sequence": 10,
                "field_description": "Name",
                "ttype": "char",
            },
        }
        model_ceppp_competence = code_generator_id.add_update_model(
            model_model,
            model_name,
            dct_field=dct_field,
            dct_model=dct_model,
        )

        # Add/Update Ceppp Formation
        model_model = "ceppp.formation"
        model_name = "ceppp_formation"
        dct_model = {
            "description": "ceppp_formation",
        }
        dct_field = {
            "name": {
                "code_generator_form_simple_view_sequence": 10,
                "code_generator_sequence": 2,
                "code_generator_tree_view_sequence": 10,
                "field_description": "Name",
                "ttype": "char",
            },
        }
        model_ceppp_formation = code_generator_id.add_update_model(
            model_model,
            model_name,
            dct_field=dct_field,
            dct_model=dct_model,
        )

        # Add/Update Ceppp Implication
        model_model = "ceppp.implication"
        model_name = "ceppp_implication"
        dct_model = {
            "description": "ceppp_implication",
        }
        dct_field = {
            "name": {
                "code_generator_form_simple_view_sequence": 10,
                "code_generator_sequence": 2,
                "code_generator_tree_view_sequence": 10,
                "field_description": "Name",
                "ttype": "char",
            },
        }
        model_ceppp_implication = code_generator_id.add_update_model(
            model_model,
            model_name,
            dct_field=dct_field,
            dct_model=dct_model,
        )

        # Add/Update Ceppp Langue
        model_model = "ceppp.langue"
        model_name = "ceppp_langue"
        dct_model = {
            "description": "ceppp_langue",
            "rec_name": "nom",
        }
        dct_field = {
            "nom": {
                "code_generator_form_simple_view_sequence": 10,
                "code_generator_sequence": 3,
                "code_generator_tree_view_sequence": 10,
                "field_description": "Nom",
                "ttype": "char",
            },
        }
        model_ceppp_langue = code_generator_id.add_update_model(
            model_model,
            model_name,
            dct_field=dct_field,
            dct_model=dct_model,
        )

        # Add/Update Ceppp Maladie
        model_model = "ceppp.maladie"
        model_name = "ceppp_maladie"
        dct_model = {
            "description": "ceppp_maladie",
            "rec_name": "nom",
        }
        dct_field = {
            "chapitre_maladie_id": {
                "code_generator_form_simple_view_sequence": 11,
                "code_generator_sequence": 4,
                "code_generator_tree_view_sequence": 11,
                "field_description": "Chapitre maladie",
                "relation": "ceppp.chapitre_maladie",
                "ttype": "many2one",
            },
            "nom": {
                "code_generator_form_simple_view_sequence": 10,
                "code_generator_sequence": 3,
                "code_generator_tree_view_sequence": 10,
                "field_description": "Nom",
                "ttype": "char",
            },
        }
        model_ceppp_maladie = code_generator_id.add_update_model(
            model_model,
            model_name,
            dct_field=dct_field,
            dct_model=dct_model,
        )

        # Add/Update Ceppp Maladie Proche Aidant
        model_model = "ceppp.maladie_proche_aidant"
        model_name = "ceppp_maladie_proche_aidant"
        dct_model = {
            "description": "ceppp_maladie_proche_aidant",
        }
        dct_field = {
            "name": {
                "code_generator_form_simple_view_sequence": 10,
                "code_generator_sequence": 2,
                "code_generator_tree_view_sequence": 10,
                "field_description": "Name",
                "ttype": "char",
            },
        }
        model_ceppp_maladie_proche_aidant = code_generator_id.add_update_model(
            model_model,
            model_name,
            dct_field=dct_field,
            dct_model=dct_model,
        )

        # Add/Update Ceppp Maladie Soi Meme
        model_model = "ceppp.maladie_soi_meme"
        model_name = "ceppp_maladie_soi_meme"
        dct_model = {
            "description": "ceppp_maladie_soi_meme",
        }
        dct_field = {
            "name": {
                "code_generator_form_simple_view_sequence": 10,
                "code_generator_sequence": 2,
                "code_generator_tree_view_sequence": 10,
                "field_description": "Name",
                "ttype": "char",
            },
        }
        model_ceppp_maladie_soi_meme = code_generator_id.add_update_model(
            model_model,
            model_name,
            dct_field=dct_field,
            dct_model=dct_model,
        )

        # Add/Update Ceppp Mode Communication Privilegie
        model_model = "ceppp.mode_communication_privilegie"
        model_name = "ceppp_mode_communication_privilegie"
        dct_model = {
            "description": "ceppp_mode_communication_privilegie",
        }
        dct_field = {
            "name": {
                "code_generator_form_simple_view_sequence": 10,
                "code_generator_sequence": 2,
                "code_generator_tree_view_sequence": 10,
                "field_description": "Name",
                "ttype": "char",
            },
        }
        model_ceppp_mode_communication_privilegie = (
            code_generator_id.add_update_model(
                model_model,
                model_name,
                dct_field=dct_field,
                dct_model=dct_model,
            )
        )

        # Add/Update Ceppp Occupation
        model_model = "ceppp.occupation"
        model_name = "ceppp_occupation"
        dct_model = {
            "description": "ceppp_occupation",
        }
        dct_field = {
            "name": {
                "code_generator_form_simple_view_sequence": 10,
                "code_generator_sequence": 2,
                "code_generator_tree_view_sequence": 10,
                "field_description": "Name",
                "ttype": "char",
            },
        }
        model_ceppp_occupation = code_generator_id.add_update_model(
            model_model,
            model_name,
            dct_field=dct_field,
            dct_model=dct_model,
        )

        # Add/Update Ceppp Patient
        model_model = "ceppp.patient"
        model_name = "ceppp_patient"
        dct_model = {
            "description": "ceppp_patient",
            "rec_name": "uuid",
        }
        dct_field = {
            "centre_recruteur": {
                "code_generator_form_simple_view_sequence": 12,
                "code_generator_sequence": 7,
                "field_description": "Centre de recrutement",
                "help": "Affiliation",
                "ttype": "char",
            },
            "name": {
                "code_generator_sequence": 3,
                "field_description": "Name",
                "ttype": "char",
            },
            "recruteur_id": {
                "code_generator_sequence": 4,
                "field_description": "Link recruteur",
                "relation": "ceppp.recruteur",
                "ttype": "many2one",
            },
            "recruteur_partner_id": {
                "code_generator_form_simple_view_sequence": 11,
                "code_generator_sequence": 6,
                "field_description": "Recruteur",
                "help": "Partner-related data of the user",
                "relation": "res.partner",
                "ttype": "many2one",
            },
            "uuid": {
                "code_generator_form_simple_view_sequence": 10,
                "code_generator_sequence": 5,
                "code_generator_tree_view_sequence": 10,
                "field_description": "Code",
                "help": "Identifiant unique anonymisé.",
                "ttype": "char",
            },
        }
        model_ceppp_patient = code_generator_id.add_update_model(
            model_model,
            model_name,
            dct_field=dct_field,
            dct_model=dct_model,
        )

        # Generate code
        if True:
            # Generate code header
            value = {
                "code": """from uuid import uuid4

from odoo import _, api, fields, models""",
                "name": "header",
                "m2o_module": code_generator_id.id,
                "m2o_model": model_ceppp_patient.id,
            }
            env["code.generator.model.code.import"].create(value)

        # Add/Update Ceppp Recruteur
        model_model = "ceppp.recruteur"
        model_name = "ceppp_recruteur"
        lst_depend_model = ["mail.thread", "mail.activity.mixin"]
        dct_model = {
            "description": "ceppp_recruteur",
            "enable_activity": True,
        }
        dct_field = {
            "active": {
                "code_generator_form_simple_view_sequence": 10,
                "code_generator_sequence": 3,
                "default": True,
                "field_description": "Actif",
                "force_widget": "boolean_button",
                "help": (
                    "Lorsque non actif, ce patient n'est plus en fonction,"
                    " mais demeure accessible."
                ),
                "ttype": "boolean",
            },
            "adresse_postale": {
                "code_generator_sequence": 15,
                "field_description": "Adresse postale",
                "ttype": "char",
            },
            "centre_recruteur": {
                "code_generator_form_simple_view_sequence": 16,
                "code_generator_sequence": 13,
                "field_description": "Centre de recrutement",
                "help": "Affiliation",
                "ttype": "char",
            },
            "commentaires": {
                "code_generator_form_simple_view_sequence": 32,
                "code_generator_sequence": 33,
                "field_description": "Commnentaires",
                "ttype": "text",
            },
            "competence_patient": {
                "code_generator_form_simple_view_sequence": 31,
                "code_generator_sequence": 32,
                "field_description": "Compétences au partenariat",
                "help": "Compétences du patient.",
                "relation": "ceppp.competence",
                "ttype": "many2many",
            },
            "consentement_notification": {
                "code_generator_form_simple_view_sequence": 28,
                "code_generator_sequence": 10,
                "field_description": (
                    "Consentement aux notifications/communications"
                ),
                "ttype": "boolean",
            },
            "consentement_recherche": {
                "code_generator_form_simple_view_sequence": 30,
                "code_generator_sequence": 12,
                "field_description": "Consentement à la recherche",
                "help": (
                    "Consentement dans le cadre d'activités de recherche sur"
                    " le partenariat."
                ),
                "ttype": "boolean",
            },
            "consentement_recrutement": {
                "code_generator_form_simple_view_sequence": 29,
                "code_generator_sequence": 11,
                "field_description": "Consentement au recrutement",
                "help": (
                    "Consentement dans le cadre d'activités de partenariat. Si"
                    " vous voulez vous retirer en tant que patient partenaire,"
                    " veuillez envoyer un courriel à cette adresse <mail -"
                    " formulaire prérempli?>"
                ),
                "ttype": "boolean",
            },
            "courriel": {
                "code_generator_sequence": 14,
                "field_description": "Adresse courriel",
                "ttype": "char",
            },
            "date_naissance": {
                "code_generator_form_simple_view_sequence": 17,
                "code_generator_sequence": 19,
                "field_description": "Date de naissance",
                "help": (
                    "Permet de connaître le groupe d'âge pour des implications"
                    " spécifiques."
                ),
                "ttype": "date",
            },
            "formation_professionnelle": {
                "code_generator_form_simple_view_sequence": 33,
                "code_generator_sequence": 26,
                "field_description": "Formation professionnelle",
                "help": "Plus haut diplôme obtenu et domaine",
                "ttype": "char",
            },
            "genre": {
                "code_generator_form_simple_view_sequence": 19,
                "code_generator_sequence": 22,
                "field_description": "Genre",
                "help": (
                    "Le genre fait référence aux rôles, aux comportements, aux"
                    " expressions et aux identités des filles, des femmes, des"
                    " garçons, des hommes et des personnes de diverses"
                    " identités de genre. Le genre influence la perception que"
                    " les individus ont d'eux-mêmes ou d'autrui, leur manière"
                    " d'agir ou d'interagir, ainsi que la répartition du"
                    " pouvoir et des ressources dans la société. Bien que le"
                    " genre soit habituellement conceptualisé en termes"
                    " binaires (fille/femme et garçon/homme), les individus et"
                    " les groupes comprennent, expérimentent et expriment leur"
                    " genre de diverses façons."
                ),
                "selection": (
                    "[('homme', 'Homme'), ('femme', 'Femme'),"
                    " ('bispirituelle', 'Bispirituel.le'), ('autre', 'Autre')]"
                ),
                "ttype": "selection",
            },
            "genre_autre": {
                "code_generator_form_simple_view_sequence": 20,
                "code_generator_sequence": 23,
                "field_description": "Autre genre",
                "help": (
                    "Peut être défini lorsque le genre est au choix 'autre'."
                ),
                "ttype": "char",
            },
            "heritage_culturel": {
                "code_generator_form_simple_view_sequence": 21,
                "code_generator_sequence": 27,
                "field_description": "Héritage culturel",
                "help": (
                    "Est-ce que vous vous identifiez comme membre d'une"
                    " minorité visible, au sens de la Loi sur l'équité en"
                    " matière d'emploi. Selon cette loi, les personnes, autres"
                    " que les Premiers Peuples, qui ne sont pas caucasiens ou"
                    " qui n'ont pas la peau blanche font partie des minorités"
                    " visibles. À cela s'ajoute également l'héritage culturel"
                    " associées aux minorités visibles comme les pratiques,"
                    " représentations, expressions, connaissances et"
                    " savoir-faire - ainsi que les instruments, objets,"
                    " artefacts et espaces culturels qui leur sont associés -"
                    " que les communautés, les groupes et, le cas échéant, les"
                    " individus reconnaissent comme faisant partie de leur"
                    " patrimoine culturel. Ce patrimoine culturel immatériel,"
                    " transmis de génération en génération, est recréé en"
                    " permanence par les communautés et groupes en fonction de"
                    " leur milieu, de leur interaction avec la nature et de"
                    " leur histoire, et leur procure un sentiment d’identité"
                    " et de continuité, contribuant ainsi à promouvoir le"
                    " respect de la diversité culturelle et la créativité"
                    " humaine (Référence:"
                    " https://ich.unesco.org/fr/convention#art2)."
                ),
                "selection": (
                    "[('oui', 'Oui'), ('non', 'Non'), ('ne_pas_repondre',"
                    " 'Préfère ne pas répondre')]"
                ),
                "ttype": "selection",
            },
            "image": {
                "code_generator_form_simple_view_sequence": 11,
                "code_generator_sequence": 5,
                "field_description": "Image",
                "force_widget": "image",
                "help": (
                    "This field holds the image used as avatar for this"
                    " contact, limited to 1024x1024px"
                ),
                "ttype": "binary",
            },
            "image_medium": {
                "code_generator_sequence": 6,
                "field_description": "Medium-sized image",
                "help": (
                    "Medium-sized image of this contact. It is automatically"
                    " resized as a 128x128px image, with aspect ratio"
                    " preserved. Use this field in form views or some kanban"
                    " views."
                ),
                "ttype": "binary",
            },
            "image_small": {
                "code_generator_sequence": 7,
                "field_description": "Small-sized image",
                "help": (
                    "Small-sized image of this contact. It is automatically"
                    " resized as a 64x64px image, with aspect ratio preserved."
                    " Use this field anywhere a small image is required."
                ),
                "ttype": "binary",
            },
            "langue_parle_ecrit": {
                "code_generator_form_simple_view_sequence": 22,
                "code_generator_sequence": 28,
                "field_description": "Langues parlées/écrites",
                "relation": "ceppp.langue",
                "ttype": "many2many",
            },
            "langue_parle_ecrit_autre": {
                "code_generator_form_simple_view_sequence": 23,
                "code_generator_sequence": 29,
                "field_description": "Autre langues parlées/écrites",
                "help": (
                    "Peut être défini lorsque la langue parlées/écrites est au"
                    " choix 'autre'."
                ),
                "ttype": "char",
            },
            "mobile": {
                "code_generator_sequence": 17,
                "field_description": "Téléphone mobile",
                "ttype": "char",
            },
            "mode_communication_privilegie": {
                "code_generator_form_simple_view_sequence": 24,
                "code_generator_sequence": 30,
                "field_description": "Mode de communication privilégié",
                "relation": "ceppp.mode_communication_privilegie",
                "ttype": "many2many",
            },
            "name": {
                "code_generator_form_simple_view_sequence": 12,
                "code_generator_sequence": 4,
                "code_generator_tree_view_sequence": 10,
                "field_description": "Name",
                "ttype": "char",
            },
            "occupation": {
                "code_generator_form_simple_view_sequence": 26,
                "code_generator_sequence": 24,
                "field_description": "Occupation",
                "help": "Occupation principale du temps",
                "relation": "ceppp.occupation",
                "ttype": "many2many",
            },
            "occupation_autre": {
                "code_generator_form_simple_view_sequence": 27,
                "code_generator_sequence": 25,
                "field_description": "Autre occupation",
                "help": (
                    "Peut être défini lorsque l'occupation est au choix"
                    " 'autre'."
                ),
                "ttype": "char",
            },
            "patient_actif": {
                "code_generator_form_simple_view_sequence": 25,
                "code_generator_sequence": 31,
                "field_description": "Patient actif-passif",
                "help": (
                    "Actif: patient partenaire est disponible à participer"
                    " dans des projets. Passif: patient partenaire n'est pas"
                    " disponible à participer dans des projets."
                ),
                "selection": "[('actif', 'Actif'), ('passif', 'Passif')]",
                "ttype": "selection",
            },
            "patient_partner_id": {
                "code_generator_form_simple_view_sequence": 13,
                "code_generator_sequence": 20,
                "field_description": "Patient",
                "relation": "res.partner",
                "ttype": "many2one",
            },
            "recruteur_partner_id": {
                "code_generator_form_simple_view_sequence": 14,
                "code_generator_sequence": 8,
                "field_description": "Recruteur",
                "help": "Partner-related data of the user",
                "relation": "res.partner",
                "ttype": "many2one",
            },
            "recruteur_user_id": {
                "code_generator_form_simple_view_sequence": 15,
                "code_generator_sequence": 9,
                "field_description": "Recruteur user",
                "relation": "res.users",
                "ttype": "many2one",
            },
            "sexe": {
                "code_generator_form_simple_view_sequence": 18,
                "code_generator_sequence": 21,
                "field_description": "Sexe",
                "help": (
                    "Le sexe fait référence à un ensemble de caractéristiques"
                    " biologiques chez les humains et les animaux. Ces"
                    " caractéristiques physiques ou physiologiques concernent"
                    " principalement les chromosomes, l’expression des gènes,"
                    " les niveaux d’hormones et leur fonction, ainsi que"
                    " l’anatomie de l’appareil reproducteur. Le sexe comporte"
                    " habituellement deux catégories (mâle, femelle);"
                    " cependant, les caractéristiques biologiques liées au"
                    " sexe et l’expression de ces caractéristiques peuvent"
                    " varier."
                ),
                "selection": (
                    "[('homme', 'Homme'), ('femme', 'Femme'), ('intersexe',"
                    " 'Intersexe'), ('null', 'Préfère ne pas répondre')]"
                ),
                "ttype": "selection",
            },
            "telephone": {
                "code_generator_sequence": 16,
                "field_description": "Téléphone",
                "ttype": "char",
            },
            "uuid": {
                "code_generator_sequence": 18,
                "field_description": "Code",
                "help": "Identifiant unique anonymisé.",
                "ttype": "char",
            },
        }
        model_ceppp_recruteur = code_generator_id.add_update_model(
            model_model,
            model_name,
            dct_field=dct_field,
            dct_model=dct_model,
            lst_depend_model=lst_depend_model,
        )

        # Generate code
        if True:
            # Generate code header
            value = {
                "code": """from uuid import uuid4

from odoo import _, api, fields, models""",
                "name": "header",
                "m2o_module": code_generator_id.id,
                "m2o_model": model_ceppp_recruteur.id,
            }
            env["code.generator.model.code.import"].create(value)

            # Generate code model
            lst_value = [
                {
                    "code": """for vals in vals_list:
    if "uuid" not in vals.keys():
        vals["uuid"] = str(uuid4())
return super(CepppRecruteur, self).create(vals_list)""",
                    "name": "create",
                    "decorator": "@api.model_create_multi",
                    "param": "self, vals_list",
                    "sequence": 0,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_ceppp_recruteur.id,
                },
            ]
            env["code.generator.model.code"].create(lst_value)

        # Add/Update Res Partner
        model_model = "res.partner"
        model_name = "res_partner"
        lst_depend_model = ["res.partner"]
        dct_field = {
            "ceppp_entity": {
                "code_generator_sequence": 2,
                "field_description": "Affiliation",
                "help": "Unique entity name to represent the contact.",
                "is_show_whitelist_model_inherit": True,
                "selection": (
                    "[('patient', 'Patient'), ('recruteur', 'Recruteur'),"
                    " ('affiliation', 'Centre de recrutement'),"
                    " ('administrateur', 'Administrateur')]"
                ),
                "ttype": "selection",
            },
        }
        dct_model = {
            "blacklist_all_ir_ui_view": True
        }
        model_res_partner = code_generator_id.add_update_model(
            model_model,
            model_name,
            dct_field=dct_field,
            dct_model=dct_model,
            lst_depend_model=lst_depend_model,
        )

        # Added one2many field, many2one need to be create before add one2many
        model_model = "ceppp.chapitre_maladie"
        dct_field = {
            "maladie_ids": {
                "field_description": "Maladies",
                "ttype": "one2many",
                "code_generator_sequence": 4,
                "code_generator_form_simple_view_sequence": 11,
                "code_generator_tree_view_sequence": 11,
                "relation": "ceppp.maladie",
                "relation_field": "chapitre_maladie_id",
            },
        }
        code_generator_id.add_update_model_one2many(model_model, dct_field)

        # Generate code
        if True:
            # Generate code header
            value = {
                "code": """from odoo import SUPERUSER_ID, _, api, fields, models, tools""",
                "name": "header",
                "m2o_module": code_generator_id.id,
                "m2o_model": model_res_partner.id,
            }
            env["code.generator.model.code.import"].create(value)

        # Generate view
        # Action generate view
        wizard_view = env["code.generator.generate.views.wizard"].create(
            {
                "code_generator_id": code_generator_id.id,
                "enable_generate_all": False,
            }
        )

        wizard_view.button_generate_views()

        # Generate module
        value = {"code_generator_ids": code_generator_id.ids}
        env["code.generator.writer"].create(value)


def uninstall_hook(cr, e):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        code_generator_id = env["code.generator.module"].search(
            [("name", "=", MODULE_NAME)]
        )
        if code_generator_id:
            code_generator_id.unlink()
