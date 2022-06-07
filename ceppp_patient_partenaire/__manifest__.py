{
    "name": "Ceppp Patient Partenaire",
    "category": "Uncategorized",
    "version": "12.0.1.0",
    "author": "SantéLibre",
    "license": "AGPL-3",
    "website": "https://santelibre.ca",
    "application": True,
    "depends": ["contacts"],
    "data": [
        "security/ir.model.access.csv",
        "security/security.xml",
        "views/ceppp_patient.xml",
        "views/res_partner_views.xml",
        "views/menu.xml",
        "data/ir_attachment.xml",
    ],
    "installable": True,
}
