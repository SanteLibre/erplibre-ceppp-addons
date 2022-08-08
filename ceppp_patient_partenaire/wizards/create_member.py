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
        default=lambda self: self.env.user.partner_id,
        required=True,
    )

    email = fields.Char(required=True)

    name = fields.Char(required=True)

    @api.one
    def create_member(self):
        res_partner_data = {
            "name": self.name,
            "email": self.email,
            "company_id": self.env.ref("base.main_company").id,
            "parent_id": self.recruteur_partner_id.parent_id.id,
            "ceppp_entity": self.type_membre,
        }
        partner_id = self.env["res.partner"].create(res_partner_data)

        # TODO empty password
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
        else:
            raise Exception(f"Type membre {self.type_membre} not supported.")

        self.env["res.users"].create(res_users_data)

        if self.type_membre == "patient":
            ceppp_recruteur_data = {
                "patient_partner_id": partner_id.id,
                "recruteur_partner_id": self.recruteur_partner_id.id,
            }
            ceppp_recruteur = self.env["ceppp.recruteur"].create(
                ceppp_recruteur_data
            )

            action = self.env.ref(
                "ceppp_patient_partenaire.ceppp_patient_les_patient_affiliation_action_window"
            )
            form = self.env.ref(
                "ceppp_patient_partenaire.ceppp_recruteur_view_form"
            )
            result = action.read()[0]
            # result["views"] = [(form.id, "form")]
            result["view_id"] = form.id
            result["res_id"] = 1
            # result["view_mode"] = "form"
            # result["res_id"] = ceppp_recruteur.id
            return {
                "name": _("Fiche recruteur"),
                "res_model": "ceppp.recruteur",
                "view_type": "form",
                "view_mode": "form",
                "type": "ir.actions.act_window",
                "res_id": 1,
            }
            # return {
            #     "name": "Recruteur",
            #     "view_mode": "form",
            #     "view_type": "form",
            #     "view_id": self.env.ref("ceppp_patient_partenaire.ceppp_recruteur_view_form").id,
            #     "res_model": "ceppp.recruteur",
            #     "type": "ir.actions.act_window",
            #     "res_id": ceppp_recruteur.id,
            # }
            # return result
        else:
            action = self.env.ref(
                "ceppp_patient_partenaire.ceppp_patient_les_patient_affiliation_action_window"
            )
            form = self.env.ref(
                "ceppp_patient_partenaire.ceppp_recruteur_view_form"
            )
            result = action.read()[0]
            result["views"] = [(form.id, "form")]
            result["res_id"] = partner_id.id
            return result
