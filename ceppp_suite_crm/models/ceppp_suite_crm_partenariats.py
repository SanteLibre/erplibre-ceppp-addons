from odoo import _, api, fields, models


class CepppSuiteCrmPartenariats(models.Model):
    _name = "ceppp.suite_crm.partenariats"
    _description = "ceppp_suite_crm_partenariats"

    name = fields.Char()
