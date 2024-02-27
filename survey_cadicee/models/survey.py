from odoo import _, api, fields, models


class SurveyQuestion(models.Model):
    _inherit = "survey.question"

    question = fields.Html("Question Name", required=True, translate=True)
