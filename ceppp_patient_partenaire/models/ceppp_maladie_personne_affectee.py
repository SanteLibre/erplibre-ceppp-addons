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
        if relation_value and relation_value == [(6, False, [])]:
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

    @api.depends(
        "maladie",
        "relation",
        "relation_autre",
        "detail_maladie",
        "relation_is_autre",
    )
    def _compute_name(self):
        for record in self:
            autre_value = self.env.ref(
                "ceppp_patient_partenaire.ceppp_relation_proche_9"
            ).name
            maladie = ", ".join([a.nom.strip() for a in record.maladie])
            lst_relation = [
                a.name.strip()
                for a in record.relation
                if not autre_value == a.name
            ]
            if record.relation_autre:
                lst_relation += [record.relation_autre]
            relation = ", ".join(lst_relation)

            if not maladie:
                if record.detail_maladie:
                    maladie = record.detail_maladie[:50]
                else:
                    maladie = "Aucune maladie"
            if not relation:
                if record.relation_autre or record.relation_is_autre:
                    relation = "Autre relation"
                else:
                    relation = "Aucune relation"

            record.name = f"{maladie} - {relation}"

    @api.multi
    def update_maladie_portal(self, values):
        relation = [(6, 0, [int(a) for a in values["relation"]])]
        maladie_values = {
            "detail_maladie": values["detail_maladie"],
            "relation": relation,
            "relation_autre": values["relation_autre"],
        }
        txt_maladie = values.get("maladie")
        if txt_maladie:
            lst_search = [
                ("nom", "=", a.strip())
                for a in txt_maladie.strip().strip(";").split(";")
            ]
            if lst_search:
                lst_maladie_search = ["|"] * (len(lst_search) - 1) + lst_search
                maladies_ids = self.env["ceppp.maladie"].search(
                    lst_maladie_search
                )
                maladie_values["maladie"] = [(6, 0, maladies_ids.ids)]
        self.write(maladie_values)
