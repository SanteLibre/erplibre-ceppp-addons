import logging
import os
import sys

from odoo import SUPERUSER_ID, _, api, fields, models

_logger = logging.getLogger(__name__)


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
            "entrevues": os.path.normpath(
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
            "commentaires_recruteur": os.path.normpath(
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
            "experience_patient_partenaire": os.path.normpath(
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
            "formation": os.path.normpath(
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
            "partenariats": os.path.normpath(
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
            "patients": os.path.normpath(
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
            "perspective_patient": os.path.normpath(
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
        }

        # Validate file exist before extract AST
        for model_name, file_path in self._dct_php_model_crm.items():
            if not os.path.exists(file_path):
                raise Exception(
                    f"Missing file '{file_path}' for model '{model_name}'. Do"
                    " you have the repo"
                    " 'https://github.com/lerenardprudent/ceppp_crm.git' in"
                    f" path '{ceppp_crm_path}', read file '{readme_path}'"
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
        self._dct_parser = {
            key: self.get_node_from_file(value)
            for key, value in self._dct_php_model_crm.items()
        }

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

    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        for key, value in dct_parse.items():
            print(f"Modèle : {key}")
            i = -1
            for field_name, dct_field in value.get("fields").items():
                i += 1
                str_print = f"\t {i} - field name '{dct_field.get('name')}', "
                str_print += f"type '{dct_field.get('type')}', "
                if dct_field.get("required") == "True":
                    str_print += (
                        f"\n\t\t\trequired '{dct_field.get('required')}', "
                    )
                if dct_field.get("default"):
                    str_print += (
                        f"\n\t\t\tdefault '{dct_field.get('default')}', "
                    )
                if dct_field.get("comments"):
                    str_print += (
                        f"\n\t\t\tcomments '{dct_field.get('comments')}', "
                    )
                if dct_field.get("help"):
                    str_print += f"\n\t\t\thelp '{dct_field.get('help')}', "
                # str_print += f"size '{dct_field.get('size')}', "
                if dct_field.get("qdetail"):
                    str_print += (
                        f"\n\t\t\tqdetail '{dct_field.get('qdetail')}', "
                    )
                if dct_field.get("qdetail_en"):
                    str_print += (
                        f"\n\t\t\tqdetail_en '{dct_field.get('qdetail_en')}', "
                    )
                if dct_field.get("options"):
                    str_print += (
                        f"\n\t\t\toptions '{dct_field.get('options')}', "
                    )
                print(str_print)

    raise Exception("Not finish")
