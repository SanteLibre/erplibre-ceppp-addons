# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import base64
import csv
import datetime
import logging
import os

from odoo import SUPERUSER_ID, _, api, tools

_logger = logging.getLogger(__name__)


def pre_init_hook(cr):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})

        # Update all partner
        partners = env["res.partner"].search([("name", "=", "My Company")])
        for partner in partners:
            partner.website = "https://ceppp.ca"
            partner.name = "CEPPP"
            partner.ceppp_entity = "affiliation"
            partner.email = "info@ceppp.ca"
            partner.street = "850, rue St-Denis"
            partner.street2 = "porte S03.900"
            partner.city = "Montréal"
            partner.zip = "H2X 0A9"
            partner.country_id = env.ref("base.ca")
            partner.state_id = env["res.country.state"].search(
                [("code", "ilike", "QC")], limit=1
            )
            partner.phone = "514 890-8000 poste 15488"

        partners = env["res.partner"].search([("name", "=", "Administrator")])
        for partner in partners:
            partner.website = "https://santelibre.ca"
            partner.name = "Mathieu Benoit"
            partner.email = "mathieu.benoit@santelibre.ca"
            partner.country_id = env.ref("base.ca")
            partner.state_id = env["res.country.state"].search(
                [("code", "ilike", "QC")], limit=1
            )
            partner.ceppp_entity = "administrateur"

        # Take super admin user
        users = env["res.users"].browse(2)
        users.groups_id = [
            (
                4,
                env.ref(
                    "ceppp_patient_partenaire.group_ceppp_patient_partenaire_manager"
                ).id,
            )
        ]


def post_init_hook(cr, e):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})

        # Update all partner
        partners = env["res.partner"].search([("name", "=", "CEPPP")])
        for partner in partners:
            partner_img_attachment = env.ref(
                "ceppp_patient_partenaire.ir_attachment_logo_ceppp_svg"
            )
            with tools.file_open(
                partner_img_attachment.local_url[1:], "rb"
            ) as desc_file:
                partner.image = base64.b64encode(desc_file.read())

        value_genevieve = {
            "parent_id": partners.id,
            "name": "Geneviève David",
            "company_id": env.ref("base.main_company").id,
            "ceppp_entity": "administrateur",
            "customer": False,
            "email": "genevieve.david@ceppp.ca",
            "state_id": env["res.country.state"]
            .search([("code", "ilike", "QC")])
            .id,
            "country_id": env.ref("base.ca").id,
            "tz": "America/Montreal",
        }
        with tools.file_open(
            "ceppp_patient_partenaire_migration_csv/static/img/genevieve_david.jpg",
            "rb",
        ) as desc_file:
            value_genevieve["image"] = base64.b64encode(desc_file.read())

        partner_id_genevieve = env["res.partner"].create(value_genevieve)

        value_genevieve = {
            "login": "genevieve.david@ceppp.ca",
            "company_id": env.ref("base.main_company").id,
            "partner_id": partner_id_genevieve.id,
            "groups_id": [
                (
                    4,
                    env.ref(
                        "ceppp_patient_partenaire.group_ceppp_patient_partenaire_manager"
                    ).id,
                ),
                (4, env.ref("base.user_root").id),
                (4, env.ref("base.user_admin").id),
            ],
        }
        user_id_genevieve = env["res.users"].create(value_genevieve)

        value_santelibre = {
            "name": "SantéLibre",
            "company_id": env.ref("base.main_company").id,
            "customer": False,
            "supplier": True,
            "is_company": True,
            "state_id": env["res.country.state"]
            .search([("code", "ilike", "QC")])
            .id,
            "country_id": env.ref("base.ca").id,
            "tz": "America/Montreal",
        }
        with tools.file_open(
            "ceppp_patient_partenaire_migration_csv/static/img/logo_santelibre.png",
            "rb",
        ) as desc_file:
            value_santelibre["image"] = base64.b64encode(desc_file.read())
        partner_id_santelibre = env["res.partner"].create(value_santelibre)

        partners = env["res.partner"].search([("name", "=", "Mathieu Benoit")])
        for partner in partners:
            partner.parent_id = partner_id_santelibre.id
            with tools.file_open(
                "ceppp_patient_partenaire_migration_csv/static/img/Mathieu_Benoit.jpg",
                "rb",
            ) as desc_file:
                partner.image = base64.b64encode(desc_file.read())

        add_csv_patient(env, partner_id_genevieve)


def add_csv_patient(env, partner_id_genevieve):
    file_name_perspective = os.path.normpath(
        os.path.join(
            os.path.dirname(__file__), "data", "Patient Perspective.csv"
        )
    )
    file_name_patient = os.path.normpath(
        os.path.join(os.path.dirname(__file__), "data", "Patients.csv")
    )
    header_perspective = """"Nom","ID","Description","Assigné à","Id de l'utilisateur assigné","Date de création","Date de modification","Créé par","Modifié par","Supprimé","Perspective","Ville","Province","Code postal","Pays","Adresse","Professionnels de la santé","Expérience prise de décision relative à ses soins médicaux","Établissement de santé principal","Établissement de première ligne","Médicaments","Médicaments #2","Médicaments #3","Problématiques de santé","Expérience maladie","Je suis ou j'ai été suivi(e) dans les spécialités suivantes","Maladie rare","Preneur de décisions","Expérience comme pair aidant","Expérience maladie proche","Relation avec le patient","Spécialités de soins","Problématiques de santé 2","Établissement de santé principal 2","Établissement de première ligne 2","Rôle","Description de l&#039;expérience","Formation suivie sur le partenariat patient","Si oui, laquelle","Formation par qui","Date de formation","Expérience professionnelle dans le milieu de la santé","Précisions","Membre d&#039;une association ou comité","Laquelle","Conflits d&#039;intérêt","Lesquels","Motivations à s&#039;impliquer","Disponibilités","Préférences","Autres préférences","Durée d&#039;expérience (Années / Mois)","Modifié par (Nom)","modified_by_name_owner","modified_by_name_mod","Créé par","created_by_name_owner","created_by_name_mod","assigned_user_name_owner","assigned_user_name_mod","Patients","Patients"\n"""
    header_patient = """"Prénom","Nom de Famille","ID","Civilité","Titre","Service","Adresse(s) E-mail","E-mail(s) secondaire(s)","Portable","Téléphone","Ligne directe","Téléphone autre","Fax","Adresse principale","Adresse principale Ville","Adresse principale Région","Adresse principale Code postal","Pays (adresse principale) ","Autre adresse","Autre adresse Ville","Autre adresse Région","Autre adresse Code postal","Autre adresse Pays","Description","Ne pas appeler","Assistant","Assistant Téléphone","Utilisateur","Id de l'utilisateur assigné","Date de création","Date de modification","Modifié par","Créé par","Supprimé","Photo","Base légale","Date de révision de la base légale","Source de la base légale","XXX_NAS","Numéro d'assurance social","No. de téléphone (domicile)","No. de téléphone (travail)","No. de cellulaire","adresse_perso_city","adresse_perso_state","adresse_perso_postalcode","adresse_perso_country","adresse_perso","Nom de famille","Prénom","Adresse courriel","Date de naissance","Emploi du temps","Formation professionnelle","Autre niveau (préciser)","Origine ethnique ou culturelle","Établissement de santé principal","Code","experience_maladie","domaine_soin","domaine_soin_2","domaine_soin_3","prob_sant","prob_sant_2","prob_sant_3","med_1","med_2","med_3","Douleur chronique","Problèmes de sommeil","Problème respiratoire","etabl_sante","etabl_prem_ligne","exp_decision","Expérience maladie proche","Relation avec le patient","Spécialités de soin","Spécialité domaine de soins #2","Spécialité domaine de soins #3","Problématiques de santé","Problématique de santé #2","Problématique de santé #3","Établissement de santé principal","Établissement de première ligne","Laquelle","Conflit d&#039;intérêt","Membre d&#039;une association ou comité","Motivations à s&#039;impliquer","Disponibilités","Préférences","Durée d&#039;expérience (Années / Mois)","Expérience professionnelle dans le milieu de la santé","Description de l&#039;expérience","Formation suivie sur le partenariat patient","Si oui, laquelle","Formation par qui","Compétences","Compétences","Compétences","Habiletés","Commentaires patient","Commentaires recruteur","Langues parlées","Langue de correspondance","Mobilité","Ouïe","Vue","Niveau de fatigabilité","Autres besoins spécifiques","Établissement de recrutement","Date de la rencontre téléphonique","Responsable de l&#039;entrevue","Référence","Comment","Établissement de recrutement","Consentement sur l&#039;implication","Consentement sur la recherche","Consentement sur les données","Consentement sur la communication","État","Genre","Lequel","Testy","Centre de recrutement","Aides à la mobilité","Role","Besoin d&#039;assistance","Besoin d&#039;assistance","Description de l&#039;expérience","professionnels_sante","Expérience comme pair aidant","Précisions","Date de formation","Autres préférences","Comment vous déplacez-vous ?","test int field"\n"""
    lst_perspective = []
    lst_patient = []

    with open(file_name_perspective) as file:
        first_line_perspective = file.readline()
        if first_line_perspective != header_perspective:
            raise ValueError(
                f"Expect header '{header_perspective}' for file"
                f" {file_name_perspective}"
            )
    with open(file_name_perspective) as file:
        for line in csv.DictReader(file):
            lst_perspective.append(line)

    with open(file_name_patient) as file:
        first_line_patient = file.readline()
        if first_line_patient != header_patient:
            raise ValueError(
                f"Expect header '{header_patient}' for file"
                f" {file_name_patient}"
            )
    with open(file_name_patient) as file:
        for line in csv.DictReader(file):
            lst_patient.append(line)

    lst_patient_create_date = []
    lst_existing_email = []
    for perspective in lst_perspective:
        patient_id = perspective.get("Patients")
        # Find associate patient
        for patient in lst_patient:
            if patient.get("ID") == patient_id:
                break
        else:
            # raise Exception(f"Cannot find patient id '{patient_id}'")
            print(f"Cannot find perspective '{perspective.get('Nom')}'")
            continue

        full_name = f'{patient.get("Prénom")} {patient.get("Nom de Famille")}'
        email = patient.get("Adresse courriel")
        # Check multiple email in same field
        lst_email = [a for a in email.split(" ") if "@" in a]
        first_email = lst_email[0]
        if first_email in lst_existing_email:
            # Cannot create a user with same email
            print(
                f"Ignore '{full_name}' because duplicate email"
                f" '{first_email}', all email '{lst_email}'"
            )
            continue
        lst_existing_email.append(first_email)

        recruteur_value = {
            "recruteur_partner_id": partner_id_genevieve.id,
            "name": full_name,
            "email": first_email,
        }
        create_member = env["ceppp.create_member"].create(recruteur_value)
        result = create_member.create_member()
        ceppp_recruteur = result.get("obj_id")
        commentaire = ""
        comment_message = "Note de migration"
        lst_comment_message_error = []

        # Date création
        odoo_date = datetime.datetime.strptime(
            perspective.get("Date de création"), "%m/%d/%Y %H:%M"
        ).strftime("%Y-%m-%d %H:%M:%S")
        comment_message += f"<br />Fiche recruteur créer le {odoo_date}"
        lst_patient_create_date.append((ceppp_recruteur, odoo_date))
        if len(lst_email) > 1:
            commentaire += create_comment(
                "Autres courriels", " , ".join(lst_email[1:])
            )

        # Telephone
        telephone = patient.get("No. de téléphone (domicile)")
        if telephone:
            ceppp_recruteur.phone = telephone
        telephone_travail = patient.get("No. de téléphone (travail)")
        if telephone_travail:
            commentaire += create_comment(
                "Téléphone travail ", telephone_travail
            )
        telephone_mobile = patient.get("No. de cellulaire")
        if telephone:
            ceppp_recruteur.mobile = telephone_mobile

        # Date naissance
        date_naissance = patient.get("Date de naissance")
        if date_naissance:
            odoo_date_naissance_datetime = datetime.datetime.strptime(
                date_naissance, "%m/%d/%Y"
            )
            if 2022 - odoo_date_naissance_datetime.year > 3:
                # Ignore date from creation date, it means no date
                odoo_date_naissance = odoo_date_naissance_datetime.strftime(
                    "%Y-%m-%d"
                )
                ceppp_recruteur.date_naissance = odoo_date_naissance
            else:
                lst_comment_message_error.append("Date de naissance ignoré.")

        # Emploi
        emploi_du_temps = patient.get("Emploi du temps")
        if emploi_du_temps:
            lst_emploi = emploi_du_temps.split("&")
            lst_emploi_ids = []
            for emploi_str in lst_emploi:
                if emploi_str == "autre":
                    lst_emploi_ids.append(
                        env.ref(
                            "ceppp_patient_partenaire.ceppp_occupation_7"
                        ).id
                    )
                elif emploi_str == "emploi":
                    lst_emploi_ids.append(
                        env.ref(
                            "ceppp_patient_partenaire.ceppp_occupation_1"
                        ).id
                    )
                elif emploi_str == "proche":
                    lst_emploi_ids.append(
                        env.ref(
                            "ceppp_patient_partenaire.ceppp_occupation_5"
                        ).id
                    )
                else:
                    raise Exception(f"Cannot support emploi '{emploi_str}'")
            ceppp_recruteur.occupation = [(6, False, lst_emploi_ids)]

        # Formation
        formation_professionnelle = patient.get("Formation professionnelle")
        formation_professionnelle_autre = patient.get(
            "Autre niveau (préciser)"
        )
        if formation_professionnelle and formation_professionnelle_autre:
            ceppp_recruteur.formation_professionnelle = (
                formation_professionnelle
                + " - "
                + formation_professionnelle_autre
            )
        elif formation_professionnelle:
            ceppp_recruteur.formation_professionnelle = (
                formation_professionnelle
            )
        elif formation_professionnelle_autre:
            ceppp_recruteur.formation_professionnelle = (
                formation_professionnelle_autre
            )

        # Compétences
        competence = patient.get("Compétences")
        if competence:
            ceppp_recruteur.competence_patient = [
                (
                    6,
                    False,
                    [
                        env.ref(
                            "ceppp_patient_partenaire.ceppp_competence_5"
                        ).id
                        if competence == "fait_preuve_d_altruisme"
                        else env.ref(
                            "ceppp_patient_partenaire.ceppp_competence_1"
                        ).id
                    ],
                )
            ]

        # Langue
        langue_parle = patient.get("Langues parlées")
        if langue_parle:
            lst_langue_parle = langue_parle.split("&")
            lst_langue_id = []
            for str_langue_parle in lst_langue_parle:
                if str_langue_parle == "francais":
                    lst_langue_id.append(
                        env.ref(
                            "ceppp_patient_partenaire.ceppp_langue_francais"
                        ).id
                    )
                elif str_langue_parle == "anglais":
                    lst_langue_id.append(
                        env.ref(
                            "ceppp_patient_partenaire.ceppp_langue_anglais"
                        ).id
                    )
                elif str_langue_parle == "espagnol":
                    lst_langue_id.append(
                        env.ref(
                            "ceppp_patient_partenaire.ceppp_langue_espagnol"
                        ).id
                    )
                elif str_langue_parle == "autre":
                    lst_langue_id.append(
                        env.ref(
                            "ceppp_patient_partenaire.ceppp_langue_autre"
                        ).id
                    )
            ceppp_recruteur.langue_parle_ecrit = [(6, False, lst_langue_id)]
        langue = patient.get("Langue de correspondance")
        if langue and langue == "Anglais":
            print("Psss, anglais here")
            ceppp_recruteur.patient_partner_id.lang = "en_CA"

        # Mobilité
        mobilite = patient.get("Mobilité")
        mobilite_aide = patient.get("Aides à la mobilité")
        if mobilite and mobilite == "oui":
            str_mobilite = "oui"
            if mobilite_aide:
                str_mobilite += " - " + mobilite_aide
            commentaire += create_comment("Mobilité ", str_mobilite)

        # Déplacement
        deplacement = patient.get("Comment vous déplacez-vous ?")
        if deplacement:
            commentaire += create_comment("Déplacement", deplacement)

        # Consentement
        consentement_implication = patient.get(
            "Consentement sur l&#039;implication"
        )
        if consentement_implication and consentement_implication == "non":
            ceppp_recruteur.notification = False

        # Genre
        genre = patient.get("Genre")
        if genre:
            if genre == "Homme":
                ceppp_recruteur.genre = "homme"
            elif genre == "Femme":
                ceppp_recruteur.genre = "femme"

        # Médicaments
        medicament = perspective.get("Médicaments")
        if medicament:
            commentaire += create_comment("Médicaments", medicament)

        # Maladie
        experience_maladie = perspective.get("Expérience maladie")
        if experience_maladie:
            env["ceppp.maladie_personne_affectee"].create(
                {
                    "detail_maladie": experience_maladie.strip().strip('"'),
                    "recruteur_id": ceppp_recruteur.id,
                }
            )

        experience_maladie_proche = perspective.get(
            "Expérience maladie proche"
        )
        if experience_maladie_proche:
            env["ceppp.maladie_personne_affectee"].create(
                {
                    "detail_maladie": experience_maladie_proche.strip().strip(
                        '"'
                    ),
                    "recruteur_id": ceppp_recruteur.id,
                    "relation": [
                        (
                            6,
                            False,
                            [
                                env.ref(
                                    "ceppp_patient_partenaire.ceppp_relation_proche_9"
                                ).id
                            ],
                        )
                    ],
                }
            )

        # Établissement santé
        etablissement_sante = perspective.get(
            "Établissement de santé principal"
        )
        if etablissement_sante:
            commentaire += create_comment(
                "Établissement de santé principal", etablissement_sante
            )

        etablissement_premiere_ligne = perspective.get(
            "Établissement de première ligne"
        )
        if etablissement_premiere_ligne:
            commentaire += create_comment(
                "Établissement de première ligne", etablissement_premiere_ligne
            )

        specialiste_suivant = perspective.get(
            "Je suis ou j'ai été suivi(e) dans les spécialités suivantes"
        )
        if specialiste_suivant:
            commentaire += create_comment(
                "Je suis ou j'ai été suivi(e) dans les spécialités suivantes",
                specialiste_suivant,
            )

        experience_pair_aidant = perspective.get(
            "Expérience comme pair aidant"
        )
        if experience_pair_aidant:
            commentaire += create_comment(
                "Expérience comme proche pair aidant", experience_pair_aidant
            )

        etablissement_sante_2 = perspective.get(
            "Établissement de santé principal 2"
        )
        if etablissement_sante_2:
            commentaire += create_comment(
                "Établissement de santé principal proche",
                etablissement_sante_2,
            )

        etablissement_premiere_ligne_2 = perspective.get(
            "Établissement de première ligne 2"
        )
        if etablissement_premiere_ligne_2:
            commentaire += create_comment(
                "Établissement de première ligne proche",
                etablissement_premiere_ligne_2,
            )

        specialite_soin = perspective.get("Spécialités de soins")
        if specialite_soin:
            commentaire += create_comment(
                "Spécialités de soins", specialite_soin
            )

        # Membre association
        membre_association = perspective.get("Laquelle")
        if membre_association:
            commentaire += create_comment(
                "Membre de l'association/comité", membre_association
            )

        # Motivation à s'impliquer
        motivation_impliquer = perspective.get(
            "Motivations à s&#039;impliquer"
        )
        if motivation_impliquer:
            commentaire += create_comment(
                "Motivation à s'impliquer", motivation_impliquer
            )

        # adresse
        ville = perspective.get("Ville")
        if ville:
            ceppp_recruteur.city = ville
        code_postal = perspective.get("Code postal")
        if code_postal:
            ceppp_recruteur.zip = code_postal
        adresse = perspective.get("Adresse")
        if adresse:
            ceppp_recruteur.street = adresse

        # Comment fiche
        if commentaire:
            ceppp_recruteur.commentaires = commentaire.strip()

        # Add comment in mail.message
        if lst_comment_message_error:
            error_message = "</li><li>".join(lst_comment_message_error)
            comment_message += (
                "<br/>Erreur détecté : <br"
                f" /><ul><li>{error_message}</li></ul>"
            )

        comment_value = {
            "subject": "Note de migration - CEPPP suite CRM",
            "body": f"<p>{comment_message}</p>",
            "parent_id": False,
            "message_type": "comment",
            "author_id": env.ref("base.partner_root").id,
            "model": "ceppp.recruteur",
            "res_id": ceppp_recruteur.id,
        }
        env["mail.message"].create(comment_value)

        print(
            f"Create ceppp.recruteur id '{ceppp_recruteur.id}'. Name"
            f" '{full_name}'. Commentaire : '"
            + commentaire.replace("\n", " ")
            + f"'. Erreur : '{lst_comment_message_error}'"
        )
    # Force save transaction at the end and update create date
    env.cr.commit()
    # Update create date, ignore modified, because the actual value is true
    for ceppp_recruteur, odoo_date in lst_patient_create_date:
        print(f"Update id '{ceppp_recruteur.id}' to create_date '{odoo_date}'")
        env.cr.execute(
            "UPDATE ceppp_recruteur set create_date = '%s' WHERE id=%s"
            % (odoo_date, ceppp_recruteur.id)
        )
        env.cr.execute(
            "UPDATE ceppp_patient set create_date = '%s' WHERE id=%s"
            % (odoo_date, ceppp_recruteur.patient_partner_id.id)
        )
    # print(lst_perspective)
    # print(lst_patient)
    print("END Migration Suite CRM")


def create_comment(title, value):
    comment = ""

    value_transform = value.strip().strip('"').strip()
    # if value_transform.count("\n") >= 1:
    #     comment += "\n"
    comment += f"\n{title} : {value_transform}\n"
    # if value_transform.count("\n") >= 1:
    #     comment += "\n"

    return comment
