{
    "name": "Ceppp Patient Partenaire",
    "category": "Uncategorized",
    "version": "12.0.1.0",
    "author": "SantéLibre",
    "license": "AGPL-3",
    "website": "https://santelibre.ca",
    "application": True,
    "depends": [
        "contacts",
        "mail",
    ],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/ceppp_chapitre_maladie.xml",
        "data/ceppp_chapitre_maladie.xml",
        "views/ceppp_competence.xml",
        "data/ceppp_competence.xml",
        "views/ceppp_formation.xml",
        "views/ceppp_implication.xml",
        "views/ceppp_langue.xml",
        "data/ceppp_langue.xml",
        "views/ceppp_maladie.xml",
        "data/ceppp_maladie.xml",
        "views/ceppp_maladie_proche_aidant.xml",
        "views/ceppp_maladie_soi_meme.xml",
        "views/ceppp_mode_communication_privilegie.xml",
        "data/ceppp_mode_communication_privilegie.xml",
        "views/ceppp_occupation.xml",
        "data/ceppp_occupation.xml",
        "views/ceppp_patient.xml",
        "views/ceppp_recruteur.xml",
        "views/res_partner_views.xml",
        "views/menu.xml",
        "data/ir_attachment.xml",
    ],
    "installable": True,
    "post_init_hook": "post_init_hook",
}
