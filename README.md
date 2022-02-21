# erplibre-ceppp-addons

Centre d'Excellence sur le partenariat avec les patients et le public Canada, addons de ERPLibre

## Exécution

### Le suite_crm migrator

Itération 1, faire la migration

À la racine de ERPLibre, exécuter :

```bash
./script/db_restore.py --database code_generator
./run.sh --stop-after-init --dev all -d code_generator -i code_generator_migrator_ceppp_suite_crm -u code_generator_migrator_ceppp_suite_crm
```

Et le module `ceppp_suite_crm` sera généré.

### Installer ceppp_suite_crm pour test

Pour tester le module, à la racine de ERPLibre, exécuter :

```bash
./script/db_restore.py --database test
./run.sh --stop-after-init -d test -i ceppp_suite_crm -u ceppp_suite_crm
```

### La traduction vers l'anglais

Le fichier i18n a été généré manuellement pour accélérer le travail et mis dans le
répertoire `ceppp_suite_crm/i18n/ceppp_suite_crm.pot` et une copie sur `ceppp_suite_crm/i18n/fr_CA.po`.

Lorsqu'on exécute le `suite_crm migrator`, il crée la version en anglais sur le fichier `ceppp_suite_crm/i18n/en_CA.po`.
Il faut ensuite aller activer l'anglais sur l'instance dans Configuration/Traductions/Langues pour choisir English (CA),
code local en_CA.

## Dépendance

Le module `code_generator_migrator_ceppp_suite_crm` a besoin du repo :

- https://github.com/mathben/PHP-Parsers.git au chemin `code_generator_migrator_ceppp_suite_crm/php_parser` branche
  support_erplibre.
- https://github.com/lerenardprudent/ceppp_crm.git au chemin `code_generator_migrator_ceppp_suite_crm/ceppp_crm` branche
  master.

## Format code

From ERPLibre project:

```bash
./script/maintenance/black.sh ./addons/SanteLibre_erplibre-ceppp-addons/ --extend-exclude "/(php_parser/*|ceppp_crm)/"
.venv/bin/isort ./addons/SanteLibre_erplibre-ceppp-addons --skip php_parser --skip ceppp_crm
```
