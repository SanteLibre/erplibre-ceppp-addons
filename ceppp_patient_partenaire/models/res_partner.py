from odoo import SUPERUSER_ID, _, api, fields, models, tools
from odoo.addons.bus.models.bus_presence import AWAY_TIMER
from odoo.addons.bus.models.bus_presence import DISCONNECTION_TIMER


class ResPartner(models.Model):
    _inherit = "res.partner"

    ceppp_entity = fields.Selection(
        selection=[
            ("patient", "Patient"),
            ("recruteur", "Recruteur"),
            ("affiliation", "Centre de recrutement"),
            ("administrateur", "Administrateur"),
        ],
        string="Rôle",
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
            return name
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

    @api.model
    def im_search(self, name, limit=20):
        """ Search partner with a name and return its id, name and im_status.
            Note : the user must be logged
            :param name : the partner name to search
            :param limit : the limit of result to return
        """
        # This method is supposed to be used only in the context of channel creation or
        # extension via an invite. As both of these actions require the 'create' access
        # right, we check this specific ACL.
        if self.env['mail.channel'].check_access_rights('create', raise_exception=False):
            name = '%' + name + '%'
            excluded_partner_ids = [self.env.user.partner_id.id]
            # ADDED for CEPPP
            if self.env.user.partner_id.ceppp_entity == "patient":
                return {}
            if self.env.user.partner_id.ceppp_entity == "recruteur":
                res_partner_limit_ids = self.env['res.partner'].search(
                    [('ceppp_entity', 'not in', ['recruteur', 'administrateur'])]
                )
                # res_partner_limit_ids = self.env['res.partner'].search(
                #     ['|', ('ceppp_entity', 'not in', ['recruteur', 'administrateur']),
                #      ('commercial_partner_id', '!=', self.env.user.partner_id.commercial_partner_id.id)]
                # )
                excluded_partner_ids += res_partner_limit_ids.ids
            # END ADDED for CEPPP
            self.env.cr.execute("""
                SELECT
                    U.id as user_id,
                    P.id as id,
                    P.name as name,
                    CASE WHEN B.last_poll IS NULL THEN 'offline'
                         WHEN age(now() AT TIME ZONE 'UTC', B.last_poll) > interval %s THEN 'offline'
                         WHEN age(now() AT TIME ZONE 'UTC', B.last_presence) > interval %s THEN 'away'
                         ELSE 'online'
                    END as im_status
                FROM res_users U
                    JOIN res_partner P ON P.id = U.partner_id
                    LEFT JOIN bus_presence B ON B.user_id = U.id
                WHERE P.name ILIKE %s
                    AND P.id NOT IN %s
                    AND U.active = 't'
                LIMIT %s
            """, ("%s seconds" % DISCONNECTION_TIMER, "%s seconds" % AWAY_TIMER, name, tuple(excluded_partner_ids), limit))
            return self.env.cr.dictfetchall()
        else:
            return {}
