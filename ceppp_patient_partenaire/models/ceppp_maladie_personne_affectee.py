from odoo import _, api, fields, models


class CepppMaladiePersonneAffectee(models.Model):
    _name = "ceppp.maladie_personne_affectee"
    _description = "ceppp_maladie_personne_affectee"

    name = fields.Char(compute="_compute_name")

    maladie = fields.Many2many(
        comodel_name="ceppp.maladie",
        string="Maladies",
    )

    detail_maladie = fields.Text(
        string="Détails sur la maladie",
    )

    relation = fields.Many2many(
        comodel_name="ceppp.relation_proche",
        string="Personne affectée par cette maladie",
    )

    recruteur_id = fields.Many2one(
        comodel_name="ceppp.recruteur",
    )

    relation_autre = fields.Char(string="Autre relation")

    relation_is_autre = fields.Boolean(compute="_compute_relation_is_autre")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if "relation" not in vals.keys():
                # Add me when empty
                vals["relation"] = [
                    (
                        4,
                        self.env.ref(
                            "ceppp_patient_partenaire.ceppp_relation_proche_0"
                        ).id,
                    )
                ]
        return super(CepppMaladiePersonneAffectee, self).create(vals_list)

    @api.multi
    def write(self, vals):
        relation_value = vals.get("relation")
        if relation_value and relation_value == [[6, False, []]]:
            vals["relation"] = [
                (
                    6,
                    False,
                    [
                        self.env.ref(
                            "ceppp_patient_partenaire.ceppp_relation_proche_0"
                        ).id
                    ],
                )
            ]
        return super(CepppMaladiePersonneAffectee, self).write(vals)

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
