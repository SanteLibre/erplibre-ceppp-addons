from odoo import _, api, fields, models


class CepppModeCommunicationPrivilegie(models.Model):
    _name = "ceppp.mode_communication_privilegie"
    _description = "ceppp_mode_communication_privilegie"
    _order = "sequence, id"

    name = fields.Char()

    sequence = fields.Integer(default=1, help="Order the list")
