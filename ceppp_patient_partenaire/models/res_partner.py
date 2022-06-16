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

    def _get_contact_name(self, partner, name):
        if partner.ceppp_entity:
            return "%s, %s, %s" % (
                partner.commercial_company_name or partner.parent_id.name,
                partner.ceppp_entity.title(),
                name,
            )
        return super(ResPartner, self)._get_contact_name(partner, name)

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
