# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import SUPERUSER_ID, _, api, tools

_logger = logging.getLogger(__name__)


def post_init_hook(cr, e):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})

        _logger.info(
            "Deactivating legacy access rules related to private addresses."
        )
        # env.ref("base.res_partner_rule_private_employee").active = False

        _logger.info("Force CEPPP app to be first in menu")
        menus = env["ir.ui.menu"].search(
            [
                ("parent_id", "=", False),
                ("name", "=", "Ceppp Patient Partenaire"),
            ]
        )
        menus.write({"sequence": -10})
