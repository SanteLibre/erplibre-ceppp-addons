from odoo import _, api, fields, models


class CepppLangue(models.Model):
    _name = "ceppp.langue"
    _description = "ceppp_langue"
    _order = "sequence, id"
    _rec_name = "nom"

    nom = fields.Char()

    sequence = fields.Integer(default=1, help="Order the list")
