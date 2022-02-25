from odoo import _, api, fields, models


class CepppSuiteCrmDisponibilites(models.Model):
    _name = "ceppp.suite_crm.disponibilites"
    _description = "ceppp_suite_crm_disponibilites"
    _rec_name = "nom"

    nom = fields.Char(translate=True)
