from odoo import _, api, fields, models


class CepppMaladiePersonneAffectee(models.Model):
    _name = "ceppp.maladie_personne_affectee"
    _description = "ceppp_maladie_personne_affectee"

    name = fields.Char(compute="_compute_name", store=True)

    maladie = fields.Many2many(
        comodel_name="ceppp.maladie",
        string="Maladies",
    )

    autre_maladie = fields.Char(
        string="Autres maladies",
        help="Les maladies qui ne sont pas reconnues dans la liste.",
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

    relation_is_autre = fields.Boolean(
        compute="_compute_relation_is_autre", store=True
    )

    is_me = fields.Boolean(compute="_compute_relation_is_me", store=True)

    is_proche_aidant = fields.Boolean(
        compute="_compute_relation_is_me", store=True
    )

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

    @api.depends("relation", "relation_is_autre")
    def _compute_relation_is_me(self):
        relation_moi_id = self.env.ref(
            "ceppp_patient_partenaire.ceppp_relation_proche_0"
        )
        for record in self:
            # is_me if missing relation or relation contains "me"
            record.is_me = (
                record.relation is False and record.relation_is_autre is False
            ) or (
                record.relation and relation_moi_id.id in record.relation.ids
            )
            # is_proche_aidant if any relation except "me" or other_relation
            record.is_proche_aidant = record.relation_is_autre or any(
                set(record.relation.ids) - {relation_moi_id.id}
            )

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
        if "maladie" in values.keys():
            txt_maladie = values.get("maladie")
            lst_txt_maladie = txt_maladie.strip().strip(";").split(";")
            lst_search = [("nom", "=", a.strip()) for a in lst_txt_maladie]
            if lst_search:
                lst_maladie_search = ["|"] * (len(lst_search) - 1) + lst_search
                maladies_ids = self.env["ceppp.maladie"].search(
                    lst_maladie_search
                )
                maladie_values["maladie"] = [(6, 0, maladies_ids.ids)]
                # Compute not found fields
                lst_not_found = [
                    a.strip()
                    for a in lst_txt_maladie
                    if a not in [b.nom for b in maladies_ids]
                ]
                maladie_values["autre_maladie"] = "; ".join(lst_not_found)
            else:
                # Erase it
                maladie_values["maladie"] = [(5,)]
                maladie_values["autre_maladie"] = ""
        self.write(maladie_values)
