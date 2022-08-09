from odoo import SUPERUSER_ID, _, api, fields, models, tools


class ResPartner(models.Model):
    _inherit = "res.partner"

    ceppp_entity = fields.Selection(
        selection=[
            ("patient", "Patient"),
            ("recruteur", "Recruteur"),
            ("affiliation", "Centre de recrutement"),
            ("administrateur", "Administrateur"),
        ],
        string="Affiliation",
        help="Unique entity name to represent the contact.",
    )

    patient_partner_ids = fields.One2many(
        comodel_name="ceppp.recruteur",
        string="Patient",
        inverse_name="patient_partner_id",
    )

    email = fields.Char(track_visibility="onchange")

    zip = fields.Char(track_visibility="onchange")

    phone = fields.Char(track_visibility="onchange")

    mobile = fields.Char(track_visibility="onchange")

    street = fields.Char(track_visibility="onchange")

    street2 = fields.Char(track_visibility="onchange")

    city = fields.Char(track_visibility="onchange")

    state_id = fields.Many2one(track_visibility="onchange")

    country_id = fields.Many2one(track_visibility="onchange")

    def _get_contact_name(self, partner, name):
        if partner.ceppp_entity:
            return "%s, %s, %s" % (
                partner.commercial_company_name or partner.parent_id.name,
                partner.ceppp_entity.title(),
                name,
            )
        return super(ResPartner, self)._get_contact_name(partner, name)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if (
                "ceppp_entity" in vals.keys()
                and vals["ceppp_entity"] == "patient"
            ):
                # Force type address for custom personal
                vals["type"] = "private"
        return super(ResPartner, self).create(vals_list)

    @api.multi
    def write(self, vals):
        if "ceppp_entity" in vals.keys() and vals["ceppp_entity"] == "patient":
            # Force type address for custom personal
            vals["type"] = "private"
        return super(ResPartner, self).write(vals)

    @api.depends(
        "is_company",
        "name",
        "parent_id.name",
        "type",
        "company_name",
        "ceppp_entity",
    )
    def _compute_display_name(self):
        super(ResPartner, self)._compute_display_name()

    def open_fiche_recruteur(self):
        if self.patient_partner_ids:
            return {
                "name": _("Fiche recruteur"),
                "res_model": "ceppp.recruteur",
                "view_type": "form",
                "view_mode": "form",
                "type": "ir.actions.act_window",
                "res_id": self.patient_partner_ids.ids[0],
            }
