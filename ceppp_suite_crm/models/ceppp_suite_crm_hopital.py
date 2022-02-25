from odoo import _, api, fields, models


class CepppSuiteCrmHopital(models.Model):
    _name = "ceppp.suite_crm.hopital"
    _description = "ceppp_suite_crm_hopital"
    _rec_name = "nom"

    nom = fields.Char(translate=True)

    region_admin_id = fields.Many2one(
        comodel_name="ceppp.suite_crm.region_admin",
        string="Région administrative",
    )
