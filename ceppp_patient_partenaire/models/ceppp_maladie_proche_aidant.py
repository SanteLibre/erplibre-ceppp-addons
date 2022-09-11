from odoo import _, api, fields, models


class CepppMaladieProcheAidant(models.Model):
    _name = "ceppp.maladie_proche_aidant"
    _description = "ceppp_maladie_proche_aidant"

    name = fields.Char(compute="_compute_name")

    maladie = fields.Many2many(
        comodel_name="ceppp.maladie",
        string="Maladies",
    )

    autre_maladie = fields.Text(
        string="Autre maladie",
    )

    relation = fields.Many2many(
        comodel_name="ceppp.relation_proche",
        string="Relation avec la personne aidée",
    )

    recruteur_id = fields.Many2one(
        comodel_name="ceppp.recruteur",
    )

    relation_autre = fields.Char(string="Autre relation")

    relation_is_autre = fields.Boolean(compute="_compute_relation_is_autre")

    @api.depends("relation")
    def _compute_relation_is_autre(self):
        for record in self:
            record.relation_is_autre = (
                self.env.ref(
                    "ceppp_patient_partenaire.ceppp_relation_proche_9"
                ).id
                in record.relation.ids
            )

    @api.depends("maladie", "relation", "relation_autre")
    def _compute_name(self):
        for record in self:
            autre_value = self.env.ref(
                "ceppp_patient_partenaire.ceppp_relation_proche_9"
            ).name
            maladie = ";".join([a.nom for a in record.maladie])
            lst_relation = [
                a.name for a in record.relation if not autre_value == a.name
            ]
            if record.relation_autre:
                lst_relation += [record.relation_autre]
            relation = ";".join(lst_relation)

            if not maladie:
                maladie = "Aucune maladie"
            if not relation:
                relation = "Aucune relation"
            record.name = f"{maladie} - {relation}"
