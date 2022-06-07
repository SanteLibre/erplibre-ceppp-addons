{
    "name": "Demo CEPPP patient partenaire",
    "version": "12.0.1.0",
    "author": "SantéLibre",
    "license": "AGPL-3",
    "website": "https://santelibre.ca",
    "depends": ["ceppp_patient_partenaire"],
    "data": ["data/user_demo.xml", "data/ceppp_patient.xml"],
    "post_init_hook": "post_init_hook",
    "installable": True,
}
