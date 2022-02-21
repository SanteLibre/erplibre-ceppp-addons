import html
import logging
import os
import sys

import polib

from odoo import SUPERUSER_ID, _, api, fields, models

_logger = logging.getLogger(__name__)

MODULE_NAME = "ceppp_suite_crm"
MAPPING_FIELD_SUITE_CRM = {
    "date": "date",
    "varchar": "char",
    "text": "text",
    "name": "char",
    "radioenum": None,  # check options
    "SmartDropdown": None,  # Special case
    "enum": None,  # Special case
    "int": "integer",
    "phone": "char",
}

MAPPING_FIELD_OPTIONS_SUITE_CRM = {
    "yes_no_list": "boolean",
}


class PHPParser:
    def __init__(self):
        # Do this to optimize execution speed, only import when create this class
        self._import()
        self._extract_ast()

    def _import(self):
        # Validate git repo exist
        readme_path = os.path.normpath(
            os.path.join(os.path.dirname(__file__), "..", "README.md")
        )
        php_parser_path = os.path.normpath(
            os.path.join(os.path.dirname(__file__), "php_parser")
        )
        if not os.path.exists(php_parser_path):
            raise Exception(
                "Missing repo 'https://github.com/mathben/PHP-Parsers.git' in"
                f" path '{php_parser_path}', read file '{readme_path}'"
            )
        sys.path.append(php_parser_path)

        ceppp_crm_path = os.path.normpath(
            os.path.join(os.path.dirname(__file__), "ceppp_crm")
        )
        if not os.path.exists(ceppp_crm_path):
            readme_path = os.path.normpath(
                os.path.join(os.path.dirname(__file__), "..", "README.md")
            )
            raise Exception(
                "Missing repo"
                " 'https://github.com/lerenardprudent/ceppp_crm.git' in path"
                f" '{ceppp_crm_path}', read file '{readme_path}'"
            )

        # List of php file to extract
        self._dct_php_model_crm = {
            "entrevues": {
                "var": os.path.normpath(
                    os.path.join(
                        os.path.dirname(__file__),
                        "ceppp_crm",
                        "custom",
                        "modulebuilder",
                        "builds",
                        "Entrevues",
                        "SugarModules",
                        "modules",
                        "ent_Entrevues",
                        "vardefs.php",
                    )
                ),
                "var_fr": os.path.normpath(
                    os.path.join(
                        os.path.dirname(__file__),
                        "ceppp_crm",
                        "custom",
                        "modulebuilder",
                        "builds",
                        "Entrevues",
                        "SugarModules",
                        "modules",
                        "ent_Entrevues",
                        "language",
                        "fr_FR.lang.php",
                    )
                ),
                "var_en": os.path.normpath(
                    os.path.join(
                        os.path.dirname(__file__),
                        "ceppp_crm",
                        "custom",
                        "modulebuilder",
                        "builds",
                        "Entrevues",
                        "SugarModules",
                        "modules",
                        "ent_Entrevues",
                        "language",
                        "en_us.lang.php",
                    )
                ),
            },
            "commentaires_recruteur": {
                "var": os.path.normpath(
                    os.path.join(
                        os.path.dirname(__file__),
                        "ceppp_crm",
                        "custom",
                        "modulebuilder",
                        "builds",
                        "Patients",
                        "SugarModules",
                        "modules",
                        "pat_CommentairesRecruteur",
                        "vardefs.php",
                    )
                ),
                "var_fr": os.path.normpath(
                    os.path.join(
                        os.path.dirname(__file__),
                        "ceppp_crm",
                        "custom",
                        "modulebuilder",
                        "builds",
                        "Patients",
                        "SugarModules",
                        "modules",
                        "pat_CommentairesRecruteur",
                        "language",
                        "fr_FR.lang.php",
                    )
                ),
                "var_en": os.path.normpath(
                    os.path.join(
                        os.path.dirname(__file__),
                        "ceppp_crm",
                        "custom",
                        "modulebuilder",
                        "builds",
                        "Patients",
                        "SugarModules",
                        "modules",
                        "pat_CommentairesRecruteur",
                        "language",
                        "en_us.lang.php",
                    )
                ),
            },
            "exp_patient_partenaire": {
                "var": os.path.normpath(
                    os.path.join(
                        os.path.dirname(__file__),
                        "ceppp_crm",
                        "custom",
                        "modulebuilder",
                        "builds",
                        "Patients",
                        "SugarModules",
                        "modules",
                        "pat_ExperiencePatientPartenaire",
                        "vardefs.php",
                    )
                ),
                "var_fr": os.path.normpath(
                    os.path.join(
                        os.path.dirname(__file__),
                        "ceppp_crm",
                        "custom",
                        "modulebuilder",
                        "builds",
                        "Patients",
                        "SugarModules",
                        "modules",
                        "pat_ExperiencePatientPartenaire",
                        "language",
                        "fr_FR.lang.php",
                    )
                ),
                "var_en": os.path.normpath(
                    os.path.join(
                        os.path.dirname(__file__),
                        "ceppp_crm",
                        "custom",
                        "modulebuilder",
                        "builds",
                        "Patients",
                        "SugarModules",
                        "modules",
                        "pat_ExperiencePatientPartenaire",
                        "language",
                        "en_us.lang.php",
                    )
                ),
            },
            "formation": {
                "var": os.path.normpath(
                    os.path.join(
                        os.path.dirname(__file__),
                        "ceppp_crm",
                        "custom",
                        "modulebuilder",
                        "builds",
                        "Patients",
                        "SugarModules",
                        "modules",
                        "pat_Formation",
                        "vardefs.php",
                    )
                ),
                "var_fr": os.path.normpath(
                    os.path.join(
                        os.path.dirname(__file__),
                        "ceppp_crm",
                        "custom",
                        "modulebuilder",
                        "builds",
                        "Patients",
                        "SugarModules",
                        "modules",
                        "pat_Formation",
                        "language",
                        "fr_FR.lang.php",
                    )
                ),
                "var_en": os.path.normpath(
                    os.path.join(
                        os.path.dirname(__file__),
                        "ceppp_crm",
                        "custom",
                        "modulebuilder",
                        "builds",
                        "Patients",
                        "SugarModules",
                        "modules",
                        "pat_Formation",
                        "language",
                        "en_us.lang.php",
                    )
                ),
            },
            "partenariats": {
                "var": os.path.normpath(
                    os.path.join(
                        os.path.dirname(__file__),
                        "ceppp_crm",
                        "custom",
                        "modulebuilder",
                        "builds",
                        "Patients",
                        "SugarModules",
                        "modules",
                        "pat_Partenariats",
                        "vardefs.php",
                    )
                ),
                "var_fr": os.path.normpath(
                    os.path.join(
                        os.path.dirname(__file__),
                        "ceppp_crm",
                        "custom",
                        "modulebuilder",
                        "builds",
                        "Patients",
                        "SugarModules",
                        "modules",
                        "pat_Partenariats",
                        "language",
                        "fr_FR.lang.php",
                    )
                ),
                "var_en": os.path.normpath(
                    os.path.join(
                        os.path.dirname(__file__),
                        "ceppp_crm",
                        "custom",
                        "modulebuilder",
                        "builds",
                        "Patients",
                        "SugarModules",
                        "modules",
                        "pat_Partenariats",
                        "language",
                        "en_us.lang.php",
                    )
                ),
            },
            "patients": {
                "var": os.path.normpath(
                    os.path.join(
                        os.path.dirname(__file__),
                        "ceppp_crm",
                        "custom",
                        "modulebuilder",
                        "builds",
                        "Patients",
                        "SugarModules",
                        "modules",
                        "pat_Patients",
                        "vardefs.php",
                    )
                ),
                "var_fr": os.path.normpath(
                    os.path.join(
                        os.path.dirname(__file__),
                        "ceppp_crm",
                        "custom",
                        "modulebuilder",
                        "builds",
                        "Patients",
                        "SugarModules",
                        "modules",
                        "pat_Patients",
                        "language",
                        "fr_FR.lang.php",
                    )
                ),
                "var_en": os.path.normpath(
                    os.path.join(
                        os.path.dirname(__file__),
                        "ceppp_crm",
                        "custom",
                        "modulebuilder",
                        "builds",
                        "Patients",
                        "SugarModules",
                        "modules",
                        "pat_Patients",
                        "language",
                        "en_us.lang.php",
                    )
                ),
            },
            "perspective_patient": {
                "var": os.path.normpath(
                    os.path.join(
                        os.path.dirname(__file__),
                        "ceppp_crm",
                        "custom",
                        "modulebuilder",
                        "builds",
                        "Patients",
                        "SugarModules",
                        "modules",
                        "pat_PerspectivePatient",
                        "vardefs.php",
                    )
                ),
                "var_fr": os.path.normpath(
                    os.path.join(
                        os.path.dirname(__file__),
                        "ceppp_crm",
                        "custom",
                        "modulebuilder",
                        "builds",
                        "Patients",
                        "SugarModules",
                        "modules",
                        "pat_PerspectivePatient",
                        "language",
                        "fr_FR.lang.php",
                    )
                ),
                "var_en": os.path.normpath(
                    os.path.join(
                        os.path.dirname(__file__),
                        "ceppp_crm",
                        "custom",
                        "modulebuilder",
                        "builds",
                        "Patients",
                        "SugarModules",
                        "modules",
                        "pat_PerspectivePatient",
                        "language",
                        "en_us.lang.php",
                    )
                ),
            },
        }

        # Validate file exist before extract AST
        for model_name, dct_file_path in self._dct_php_model_crm.items():
            for file_type, file_path in dct_file_path.items():
                if not os.path.exists(file_path):
                    raise Exception(
                        f"Missing file '{file_path}' for model '{model_name}'"
                        f" and filetype '{file_type}'. Do you have the repo"
                        " 'https://github.com/lerenardprudent/ceppp_crm.git'"
                        f" in path '{ceppp_crm_path}', read file"
                        f" '{readme_path}'"
                    )

        # TODO change this way to import when refactor the library (who is coded in java style...)
        from src.compiler.php import phpast
        from src.modules.php.syntax_tree import build_syntax_tree
        from src.modules.php.traversers.bf import BFTraverser
        from src.modules.php.visitors.finders import NodeFinder

        self.ast_php_type = phpast
        self.build_syntax_tree = build_syntax_tree
        self.bft_traverser = BFTraverser
        self.node_finder = NodeFinder

    def _extract_ast(self):
        dct_ordered_php_model = sorted(
            self._dct_php_model_crm.items(), key=lambda x: x[0]
        )
        # Parser in alpha order
        self._dct_parser = {}
        for key, dct_php_value in dct_ordered_php_model:
            dct_value = {}
            for file_type, file_path in dct_php_value.items():
                dct_value[file_type] = self.get_node_from_file(file_path)
            self._dct_parser[key] = dct_value

    def get_dct_parse(self):
        return self._dct_parser

    def extract_assignment_array_to_dict(self, node):
        if isinstance(node, self.ast_php_type.Array):
            dct_value = {}
            # Expect it's key with value
            for sub_node in node.nodes:
                key, value = self.extract_assignment_array_to_dict(sub_node)
                dct_value[key] = value
            return dct_value
        elif isinstance(node, self.ast_php_type.ArrayElement):
            if isinstance(node.value, self.ast_php_type.Constant):
                if node.value.name == "true":
                    value = True
                elif node.value.name == "false":
                    value = False
                else:
                    raise Exception(
                        f"Not supported constant php: {node.value}"
                    )
            elif isinstance(node.value, str):
                value = node.value
            elif isinstance(node.value, int):
                value = node.value
            elif isinstance(node.value, self.ast_php_type.Array):
                value = {}
                for sub_node in node.value.nodes:
                    key, sub_value = self.extract_assignment_array_to_dict(
                        sub_node
                    )
                    value[key] = sub_value
            else:
                raise Exception(
                    f"Not supported node type : {type(node.value)}"
                )
            return node.key, value
        else:
            raise Exception(f"Not supported node type : {type(node)}")

    def get_node_from_file(self, file_path):
        tree = self.build_syntax_tree(file_path)

        bft = self.bft_traverser(tree)
        node_finder = self.node_finder(self.parser_function_has_no_params)
        bft.register_visitor(node_finder)
        bft.traverse()
        if node_finder.found:
            if len(node_finder.found) == 1:
                dct_from_node = self.extract_assignment_array_to_dict(
                    node_finder.found[0].get("node").expr
                )
                return dct_from_node
            else:
                _logger.error(
                    "Find multiple node assignment with $dictionary[''] ="
                    " array(), expect only 1. Please check code in file"
                    f" {file_path}."
                )
        else:
            _logger.error(
                f"Cannot find assignment in file {file_path}, search"
                " $dictionary[''] = array()"
            )
        return node_finder.found

    def parser_function_has_no_params(self, node):
        return isinstance(node, self.ast_php_type.Assignment)


def post_init_hook(cr, e):
    php_parser = PHPParser()
    dct_parse = php_parser.get_dct_parse()
    debug = True

    if debug:
        for key, dct_value in dct_parse.items():
            print(f"Modèle : {key}")
            for file_type, value in dct_value.items():
                i = -1
                if file_type == "var":
                    for field_name, dct_field in value.get("fields").items():
                        i += 1
                        str_print = (
                            f"\t {i} - field name '{dct_field.get('name')}', "
                        )
                        str_print += f"type '{dct_field.get('type')}', "
                        if dct_field.get("required") == "True":
                            str_print += (
                                "\n\t\t\trequired"
                                f" '{dct_field.get('required')}', "
                            )
                        if dct_field.get("default"):
                            str_print += (
                                "\n\t\t\tdefault"
                                f" '{dct_field.get('default')}', "
                            )
                        if dct_field.get("comments"):
                            str_print += (
                                "\n\t\t\tcomments"
                                f" '{dct_field.get('comments')}', "
                            )
                        if dct_field.get("help"):
                            str_print += (
                                f"\n\t\t\thelp '{dct_field.get('help')}', "
                            )
                        if dct_field.get("qdetail"):
                            str_print += (
                                "\n\t\t\tqdetail"
                                f" '{dct_field.get('qdetail')}', "
                            )
                        if dct_field.get("qdetail_en"):
                            str_print += (
                                "\n\t\t\tqdetail_en"
                                f" '{dct_field.get('qdetail_en')}', "
                            )
                        if dct_field.get("options"):
                            str_print += (
                                "\n\t\t\toptions"
                                f" '{dct_field.get('options')}', "
                            )
                        print(str_print)
                else:
                    print(f"Traduction {file_type}")
                    for sub_key, sub_value in value.items():
                        print(f"\t{sub_key} : '{sub_value}'")

    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})

        # The path of the actual file
        path_module_generate = os.path.normpath(
            os.path.join(os.path.dirname(__file__), "..")
        )

        short_name = MODULE_NAME.replace("_", " ").title()

        # Add code generator
        categ_id = env["ir.module.category"].search(
            [("name", "=", "Uncategorized")], limit=1
        )
        value = {
            "shortdesc": short_name,
            "name": MODULE_NAME,
            "license": "AGPL-3",
            "category_id": categ_id.id,
            "summary": "",
            "author": "SantéLibre",
            "website": "https://santelibre.ca",
            "application": True,
            "enable_sync_code": True,
            "path_sync_code": path_module_generate,
            "icon": os.path.join(
                os.path.dirname(__file__),
                "static",
                "description",
                "icon.png",
            ),
        }

        code_generator_id = env["code.generator.module"].create(value)

        # Search po en_CA.po if exist, and fill it, write after code generator write code
        po_en_ca = None
        i18n_dir = os.path.join(path_module_generate, MODULE_NAME, "i18n")
        po_en_ca_file_name = os.path.join(i18n_dir, "en_CA.po")
        if os.path.exists(po_en_ca_file_name):
            po_en_ca = polib.pofile(po_en_ca_file_name)

        # Add dependencies
        # code_generator_id.add_module_dependency("mail")

        prefix_model = "ceppp.suite_crm."
        # lst_depend_model = ["mail.thread", "mail.activity.mixin"]
        lst_depend_model = []
        for php_model, dct_php_value_dct_type in dct_parse.items():
            dct_php_value = dct_php_value_dct_type.get("var")
            dct_php_value_en_label = dct_php_value_dct_type.get("var_en")
            dct_php_value_fr_label = dct_php_value_dct_type.get("var_fr")
            field_rec_name = None
            model_model = f"{prefix_model}{php_model}"
            dct_field = {}
            dct_php_fields = dct_php_value.get("fields")
            if not dct_php_fields:
                _logger.warning(
                    f"Model {model_model} has no field... check value"
                    f" {dct_php_value}"
                )
            else:
                for field_name, dct_php_field_value in dct_php_fields.items():
                    suite_crm_type = dct_php_field_value.get("type")
                    new_type = MAPPING_FIELD_SUITE_CRM.get(suite_crm_type)
                    if new_type is None:
                        if suite_crm_type in ("SmartDropdown", "enum"):
                            # TODO support later
                            _logger.error(
                                f"Not support suite_crm type {suite_crm_type},"
                                f" ignore field {field_name} from model"
                                f" {model_model}"
                            )
                            continue
                        # Check option
                        suite_crm_option = dct_php_field_value.get("options")
                        if suite_crm_option:
                            new_type_from_option = (
                                MAPPING_FIELD_OPTIONS_SUITE_CRM.get(
                                    suite_crm_option
                                )
                            )
                            if new_type_from_option:
                                new_type = new_type_from_option
                            else:
                                _logger.error(
                                    "Not support suite_crm type"
                                    f" {suite_crm_type} options"
                                    f" {suite_crm_option}, ignore field"
                                    f" {field_name} from model {model_model}"
                                )
                                continue
                        else:
                            _logger.error(
                                f"Not support suite_crm type {suite_crm_type},"
                                f" ignore field {field_name} from model"
                                f" {model_model}"
                            )
                            continue

                    # Support rec_name
                    if new_type in ("char", "text") and field_rec_name is None:
                        # Take first to be rec_name
                        field_rec_name = field_name
                    if suite_crm_type == "name" or field_name == "nom":
                        # Force to use this name, a special type in suite_crm
                        field_rec_name = field_name

                    # Special type
                    if suite_crm_type == "phone":
                        # TODO force widget "phone"
                        pass

                    dct_field_info = {
                        "ttype": new_type,
                    }
                    help_value = dct_php_field_value.get("help")
                    if help_value:
                        dct_field_info["help"] = help_value
                    required = dct_php_field_value.get("required")
                    if required:
                        dct_field_info["required"] = required

                    coded_name = dct_php_field_value.get("vname")
                    # Use coded_name to find associated label
                    string_fr = dct_php_value_fr_label.get(coded_name)
                    string_en = dct_php_value_en_label.get(coded_name)
                    if not string_fr:
                        _logger.warning(
                            f"Cannot find string label for vname {coded_name},"
                            f" for field {field_name} and model {model_model}"
                        )
                    else:
                        # Transform '&amp;' to '&'
                        string_fr = html.unescape(string_fr)
                        dct_field_info["field_description"] = string_fr

                        if not string_en:
                            _logger.warning(
                                "Cannot find english string label for vname"
                                f" '{coded_name}', for field '{field_name}'"
                                f" and model {model_model}"
                            )
                        elif po_en_ca:
                            string_en = html.unescape(string_en)
                            # Search msgid and update msgstr
                            for po_entry in po_en_ca:
                                if po_entry.msgid == string_fr:
                                    po_entry.msgstr = string_en
                                    break
                            else:
                                _logger.warning(
                                    f"Cannot find translation '{string_fr}' in"
                                    f" file '{po_en_ca_file_name}' for new msg"
                                    f" '{string_en}' for field '{field_name}'"
                                    f" and model '{model_model}'"
                                )

                    dct_field[field_name] = dct_field_info

            dct_model = {}
            if field_rec_name:
                dct_model["rec_name"] = field_rec_name
            else:
                dct_field["name"] = {"ttype": "char"}
                dct_model["rec_name"] = "name"

            model_id = code_generator_id.add_update_model(
                model_model,
                dct_field=dct_field,
                dct_model=dct_model,
                lst_depend_model=lst_depend_model,
            )

        # Generate view
        # Action generate view
        wizard_view = env["code.generator.generate.views.wizard"].create(
            {
                "code_generator_id": code_generator_id.id,
                "enable_generate_all": True,
            }
        )

        wizard_view.button_generate_views()

        # Generate module
        value = {"code_generator_ids": code_generator_id.ids}
        env["code.generator.writer"].create(value)

        # Overwrite i18n en_CA.po
        if po_en_ca:
            # Create directory, because the cg write delete it
            os.mkdir(i18n_dir)
            # Create empty file to help polib
            with open(po_en_ca_file_name, "w") as fp:
                pass
            po_en_ca.save(po_en_ca_file_name)
            _logger.info(f"Write i18n en_CA on file '{po_en_ca_file_name}'.")
