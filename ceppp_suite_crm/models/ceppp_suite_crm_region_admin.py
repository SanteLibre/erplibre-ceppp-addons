from odoo import _, api, fields, models


class CepppSuiteCrmRegionAdmin(models.Model):
    _name = "ceppp.suite_crm.region_admin"
    _description = "ceppp_suite_crm_region_admin"
    _rec_name = "nom"

    nom = fields.Char(translate=True)

    hopital_ids = fields.One2many(
        comodel_name="ceppp.suite_crm.hopital",
        inverse_name="region_admin_id",
        string="Hôpitaux",
    )
