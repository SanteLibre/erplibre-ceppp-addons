from odoo import _, api, fields, models


class CepppMaladie(models.Model):
    _name = "ceppp.maladie"
    _description = "ceppp_maladie"
    _order = "sequence, id"
    _rec_name = "nom"

    nom = fields.Char(translate=True)

    chapitre_maladie_id = fields.Many2one(
        comodel_name="ceppp.chapitre_maladie",
        string="Chapitre maladie",
    )

    sequence = fields.Integer(default=1, help="Order the list")

    @api.multi
    def get_maladies_by_chapter_json(self, arg1):
        return ""
