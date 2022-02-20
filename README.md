# erplibre-ceppp-addons

Centre d'Excellence sur le partenariat avec les patients et le public Canada, addons de ERPLibre

## Dépendance

Le module `code_generator_migrator_ceppp_suite_crm` a besoin du repo :

- https://github.com/mathben/PHP-Parsers.git au chemin `code_generator_migrator_ceppp_suite_crm/php_parser` branche
  support_erplibre.
- https://github.com/lerenardprudent/ceppp_crm.git au chemin `code_generator_migrator_ceppp_suite_crm/ceppp_crm` branche
  master.

## Format code

From ERPLibre project:

- ./script/maintenance/black.sh ./addons/SanteLibre_erplibre-ceppp-addons/ --extend-exclude "/(php_parser/*|ceppp_crm)/"
- .venv/bin/isort ./addons/SanteLibre_erplibre-ceppp-addons --skip php_parser --skip ceppp_crm
