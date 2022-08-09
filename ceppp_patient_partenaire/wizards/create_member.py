import logging

from odoo import _, api, exceptions, fields, models

logger = logging.getLogger(__name__)


class CreateMember(models.TransientModel):
    _name = "ceppp.create_member"
    _description = "Create a member"

    type_membre = fields.Selection(
        selection=[
            ("patient", "Patient"),
            ("recruteur", "Recruteur"),
            ("administrateur", "Administrateur"),
        ],
        string="Type de membre",
        default="patient",
        required=True,
    )

    recruteur_partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Recruteur",
        domain="[('ceppp_entity','in',['recruteur','administrateur'])]",
        default=lambda self: self.env.user.sudo().partner_id,
        required=True,
    )

    langue = fields.Selection(
        selection=[("fr_CA", "Français"), ("en_CA", "Anglais")],
        default="fr_CA",
        required=True,
    )

    centre_recrutement_id = fields.Many2one(
        comodel_name="res.partner",
        string="Centre recrutement",
        domain="[('ceppp_entity','=','affiliation')]",
        default=lambda self: self.env.ref("base.main_company").sudo().id,
        required=True,
    )

    email = fields.Char(required=True)

    name = fields.Char(required=True)

    @api.multi
    def create_member(self):
        self.ensure_one()

        if self.type_membre not in ("patient", "recruteur", "administrateur"):
            raise Exception(f"Type membre {self.type_membre} not supported.")

        res_partner_data = {
            "name": self.name,
            "email": self.email,
            "company_id": self.env.ref("base.main_company").id,
            "ceppp_entity": self.type_membre,
        }
        if self.type_membre == "patient":
            res_partner_data[
                "parent_id"
            ] = self.recruteur_partner_id.parent_id.id
            # Can set is address
            res_partner_data["type"] = "private"
            res_partner_data["country_id"] = self.env.ref("base.ca")
        elif self.type_membre in ("recruteur", "administrateur"):
            res_partner_data["parent_id"] = self.centre_recrutement_id.id

        partner_id = self.env["res.partner"].sudo().create(res_partner_data)

        # TODO empty password
        # TODO send email to reset password
        res_users_data = {
            "partner_id": partner_id.id,
            "login": self.email,
            "password": "demo",
            "signature": f"""<span>
                --
                <br />
                {self.name}
            </span>""",
            "company_id": self.env.ref("base.main_company").id,
        }
        if self.type_membre == "patient":
            res_users_data["groups_id"] = [
                (6, 0, [self.env.ref("base.group_portal").id])
            ]
        elif self.type_membre == "recruteur":
            res_users_data["groups_id"] = [
                (
                    6,
                    0,
                    [
                        self.env.ref(
                            "ceppp_patient_partenaire.group_ceppp_patient_partenaire_recruteur"
                        ).id
                    ],
                )
            ]
        elif self.type_membre == "administrateur":
            res_users_data["groups_id"] = [
                (
                    6,
                    0,
                    [
                        self.env.ref(
                            "ceppp_patient_partenaire.group_ceppp_patient_partenaire_manager"
                        ).id
                    ],
                )
            ]

        user_id = self.env["res.users"].sudo().create(res_users_data)

        if self.type_membre == "patient":
            ceppp_recruteur_data = {
                "patient_partner_id": partner_id.id,
                "recruteur_partner_id": self.recruteur_partner_id.id,
            }
            ceppp_recruteur = (
                self.env["ceppp.recruteur"].sudo().create(ceppp_recruteur_data)
            )
            ceppp_patient = (
                self.env["ceppp.patient"]
                .sudo()
                .create({"recruteur_id": ceppp_recruteur.id})
            )
            # TODO send email to invite to portal if patient
            # self._send_email_portal(partner_id, user_id)

            action = self.env.ref(
                "ceppp_patient_partenaire.ceppp_patient_les_patient_affiliation_action_window"
            )
            form = self.env.ref(
                "ceppp_patient_partenaire.ceppp_recruteur_view_form"
            )
            result = action.read()[0]
            result["views"] = [(form.id, "form")]
            result["res_id"] = ceppp_recruteur.id
            return result
        else:
            action = self.env.ref("contacts.action_contacts")
            form = self.env.ref(
                "ceppp_patient_partenaire.view_ceppp_partner_form"
            )
            result = action.read()[0]
            result["views"] = [(form.id, "form")]
            result["res_id"] = partner_id.id
            return result

    def _send_email_portal(self, partner_id, user_id):
        # determine subject and body in the portal user's language
        template = self.env.ref("portal.mail_template_data_portal_welcome")
        wizard_id = self.env["portal.wizard"].create(
            {
                "user_ids": [(6, 0, [user_id.id])],
                "welcome_message": "Bienvenue au portail de CEPPP.",
            }
        )
        wizard_line = self.env["portal.wizard.user"].create(
            {
                "wizard_id": wizard_id.id,
                "partner_id": partner_id.id,
                "email": self.email,
                "in_portal": True,
                "user_id": user_id.id,
            }
        )
        lang = self.langue
        portal_url = partner_id.with_context(
            signup_force_type_in_url="", lang=lang
        )._get_signup_url_for_action()[partner_id.id]
        partner_id.signup_prepare()

        if template:
            template.with_context(
                dbname=self._cr.dbname, portal_url=portal_url, lang=lang
            ).send_mail(wizard_line.id, force_send=True)
        else:
            logger.warning(
                "No email template found for sending email to the portal user"
            )

        return True
