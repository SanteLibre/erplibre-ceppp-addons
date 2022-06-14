{
    "name": "Code Generator Ceppp Patient Partenaire",
    "version": "12.0.1.0",
    "author": "SantéLibre",
    "license": "AGPL-3",
    "website": "https://santelibre.ca",
    "application": True,
    "depends": [
        "code_generator",
        "code_generator_hook",
        "code_generator_portal",
        "contacts",
        "mail",
    ],
    "installable": True,
    "post_init_hook": "post_init_hook",
    "uninstall_hook": "uninstall_hook",
}
