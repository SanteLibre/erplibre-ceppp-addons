import base64
import logging

import werkzeug

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class CepppPatientPartenaireController(http.Controller):
    # @http.route("/new/res_partner", type="http", auth="user", website=True)
    # def create_new_res_partner(self, **kw):
    #     name = http.request.env.user.name
    #     email = http.request.env.user.email
    #     default_active = (
    #         http.request.env["res.partner"]
    #         .default_get(["active"])
    #         .get("active")
    #     )
    #     activity_state = (
    #         http.request.env["res.partner"]._fields["activity_state"].selection
    #     )
    #     default_activity_state = (
    #         http.request.env["res.partner"]
    #         .default_get(["activity_state"])
    #         .get("activity_state")
    #     )
    #     default_barcode = (
    #         http.request.env["res.partner"]
    #         .default_get(["barcode"])
    #         .get("barcode")
    #     )
    #     category_id = http.request.env["res.partner.category"].search(
    #         [("active", "=", True)]
    #     )
    #     lst_default_category_id = (
    #         http.request.env["res.partner"]
    #         .default_get(["category_id"])
    #         .get("category_id")
    #     )
    #     if lst_default_category_id:
    #         default_category_id = lst_default_category_id[0][2]
    #     else:
    #         default_category_id = []
    #     ceppp_entity = (
    #         http.request.env["res.partner"]._fields["ceppp_entity"].selection
    #     )
    #     default_ceppp_entity = (
    #         http.request.env["res.partner"]
    #         .default_get(["ceppp_entity"])
    #         .get("ceppp_entity")
    #     )
    #     channel_ids = http.request.env["mail.channel"].search([])
    #     lst_default_channel_ids = (
    #         http.request.env["res.partner"]
    #         .default_get(["channel_ids"])
    #         .get("channel_ids")
    #     )
    #     if lst_default_channel_ids:
    #         default_channel_ids = lst_default_channel_ids[0][2]
    #     else:
    #         default_channel_ids = []
    #     default_city = (
    #         http.request.env["res.partner"].default_get(["city"]).get("city")
    #     )
    #     default_color = (
    #         http.request.env["res.partner"].default_get(["color"]).get("color")
    #     )
    #     default_comment = (
    #         http.request.env["res.partner"]
    #         .default_get(["comment"])
    #         .get("comment")
    #     )
    #     default_commercial_company_name = (
    #         http.request.env["res.partner"]
    #         .default_get(["commercial_company_name"])
    #         .get("commercial_company_name")
    #     )
    #     commercial_partner_id = http.request.env["res.partner"].search(
    #         [("active", "=", True)]
    #     )
    #     default_commercial_partner_id = (
    #         http.request.env["res.partner"]
    #         .default_get(["commercial_partner_id"])
    #         .get("commercial_partner_id")
    #     )
    #     company_id = http.request.env["res.company"].search([])
    #     default_company_id = (
    #         http.request.env["res.partner"]
    #         .default_get(["company_id"])
    #         .get("company_id")
    #     )
    #     default_company_name = (
    #         http.request.env["res.partner"]
    #         .default_get(["company_name"])
    #         .get("company_name")
    #     )
    #     company_type = (
    #         http.request.env["res.partner"]._fields["company_type"].selection
    #     )
    #     default_company_type = (
    #         http.request.env["res.partner"]
    #         .default_get(["company_type"])
    #         .get("company_type")
    #     )
    #     default_contact_address = (
    #         http.request.env["res.partner"]
    #         .default_get(["contact_address"])
    #         .get("contact_address")
    #     )
    #     country_id = http.request.env["res.country"].search([])
    #     default_country_id = (
    #         http.request.env["res.partner"]
    #         .default_get(["country_id"])
    #         .get("country_id")
    #     )
    #     default_credit_limit = (
    #         http.request.env["res.partner"]
    #         .default_get(["credit_limit"])
    #         .get("credit_limit")
    #     )
    #     default_customer = (
    #         http.request.env["res.partner"]
    #         .default_get(["customer"])
    #         .get("customer")
    #     )
    #     default_date = (
    #         http.request.env["res.partner"].default_get(["date"]).get("date")
    #     )
    #     default_email_formatted = (
    #         http.request.env["res.partner"]
    #         .default_get(["email_formatted"])
    #         .get("email_formatted")
    #     )
    #     default_employee = (
    #         http.request.env["res.partner"]
    #         .default_get(["employee"])
    #         .get("employee")
    #     )
    #     default_function = (
    #         http.request.env["res.partner"]
    #         .default_get(["function"])
    #         .get("function")
    #     )
    #     default_im_status = (
    #         http.request.env["res.partner"]
    #         .default_get(["im_status"])
    #         .get("im_status")
    #     )
    #     industry_id = http.request.env["res.partner.industry"].search(
    #         [("active", "=", True)]
    #     )
    #     default_industry_id = (
    #         http.request.env["res.partner"]
    #         .default_get(["industry_id"])
    #         .get("industry_id")
    #     )
    #     default_is_blacklisted = (
    #         http.request.env["res.partner"]
    #         .default_get(["is_blacklisted"])
    #         .get("is_blacklisted")
    #     )
    #     default_is_company = (
    #         http.request.env["res.partner"]
    #         .default_get(["is_company"])
    #         .get("is_company")
    #     )
    #     lang = http.request.env["res.partner"]._fields["lang"].selection
    #     default_lang = (
    #         http.request.env["res.partner"].default_get(["lang"]).get("lang")
    #     )
    #     default_message_bounce = (
    #         http.request.env["res.partner"]
    #         .default_get(["message_bounce"])
    #         .get("message_bounce")
    #     )
    #     default_mobile = (
    #         http.request.env["res.partner"]
    #         .default_get(["mobile"])
    #         .get("mobile")
    #     )
    #     parent_id = http.request.env["res.partner"].search(
    #         [("active", "=", True)]
    #     )
    #     default_parent_id = (
    #         http.request.env["res.partner"]
    #         .default_get(["parent_id"])
    #         .get("parent_id")
    #     )
    #     default_parent_name = (
    #         http.request.env["res.partner"]
    #         .default_get(["parent_name"])
    #         .get("parent_name")
    #     )
    #     default_partner_share = (
    #         http.request.env["res.partner"]
    #         .default_get(["partner_share"])
    #         .get("partner_share")
    #     )
    #     default_phone = (
    #         http.request.env["res.partner"].default_get(["phone"]).get("phone")
    #     )
    #     default_ref = (
    #         http.request.env["res.partner"].default_get(["ref"]).get("ref")
    #     )
    #     self = http.request.env["res.partner"].search([("active", "=", True)])
    #     default_self = (
    #         http.request.env["res.partner"].default_get(["self"]).get("self")
    #     )
    #     default_signup_expiration = (
    #         http.request.env["res.partner"]
    #         .default_get(["signup_expiration"])
    #         .get("signup_expiration")
    #     )
    #     default_signup_token = (
    #         http.request.env["res.partner"]
    #         .default_get(["signup_token"])
    #         .get("signup_token")
    #     )
    #     default_signup_type = (
    #         http.request.env["res.partner"]
    #         .default_get(["signup_type"])
    #         .get("signup_type")
    #     )
    #     default_signup_url = (
    #         http.request.env["res.partner"]
    #         .default_get(["signup_url"])
    #         .get("signup_url")
    #     )
    #     default_signup_valid = (
    #         http.request.env["res.partner"]
    #         .default_get(["signup_valid"])
    #         .get("signup_valid")
    #     )
    #     state_id = http.request.env["res.country.state"].search([])
    #     default_state_id = (
    #         http.request.env["res.partner"]
    #         .default_get(["state_id"])
    #         .get("state_id")
    #     )
    #     default_street = (
    #         http.request.env["res.partner"]
    #         .default_get(["street"])
    #         .get("street")
    #     )
    #     default_street2 = (
    #         http.request.env["res.partner"]
    #         .default_get(["street2"])
    #         .get("street2")
    #     )
    #     default_supplier = (
    #         http.request.env["res.partner"]
    #         .default_get(["supplier"])
    #         .get("supplier")
    #     )
    #     title = http.request.env["res.partner.title"].search([])
    #     default_title = (
    #         http.request.env["res.partner"].default_get(["title"]).get("title")
    #     )
    #     type = http.request.env["res.partner"]._fields["type"].selection
    #     default_type = (
    #         http.request.env["res.partner"].default_get(["type"]).get("type")
    #     )
    #     tz = http.request.env["res.partner"]._fields["tz"].selection
    #     default_tz = (
    #         http.request.env["res.partner"].default_get(["tz"]).get("tz")
    #     )
    #     default_tz_offset = (
    #         http.request.env["res.partner"]
    #         .default_get(["tz_offset"])
    #         .get("tz_offset")
    #     )
    #     user_id = http.request.env["res.users"].search([("active", "=", True)])
    #     default_user_id = (
    #         http.request.env["res.partner"]
    #         .default_get(["user_id"])
    #         .get("user_id")
    #     )
    #     default_vat = (
    #         http.request.env["res.partner"].default_get(["vat"]).get("vat")
    #     )
    #     default_website = (
    #         http.request.env["res.partner"]
    #         .default_get(["website"])
    #         .get("website")
    #     )
    #     default_zip = (
    #         http.request.env["res.partner"].default_get(["zip"]).get("zip")
    #     )
    #     return http.request.render(
    #         "ceppp_patient_partenaire.portal_create_res_partner",
    #         {
    #             "name": name,
    #             "email": email,
    #             "activity_state": activity_state,
    #             "category_id": category_id,
    #             "ceppp_entity": ceppp_entity,
    #             "channel_ids": channel_ids,
    #             "commercial_partner_id": commercial_partner_id,
    #             "company_id": company_id,
    #             "company_type": company_type,
    #             "country_id": country_id,
    #             "industry_id": industry_id,
    #             "lang": lang,
    #             "parent_id": parent_id,
    #             "self": self,
    #             "state_id": state_id,
    #             "title": title,
    #             "type": type,
    #             "tz": tz,
    #             "user_id": user_id,
    #             "page_name": "create_res_partner",
    #             "default_active": default_active,
    #             "default_activity_state": default_activity_state,
    #             "default_barcode": default_barcode,
    #             "default_category_id": default_category_id,
    #             "default_ceppp_entity": default_ceppp_entity,
    #             "default_channel_ids": default_channel_ids,
    #             "default_city": default_city,
    #             "default_color": default_color,
    #             "default_comment": default_comment,
    #             "default_commercial_company_name": default_commercial_company_name,
    #             "default_commercial_partner_id": default_commercial_partner_id,
    #             "default_company_id": default_company_id,
    #             "default_company_name": default_company_name,
    #             "default_company_type": default_company_type,
    #             "default_contact_address": default_contact_address,
    #             "default_country_id": default_country_id,
    #             "default_credit_limit": default_credit_limit,
    #             "default_customer": default_customer,
    #             "default_date": default_date,
    #             "default_email_formatted": default_email_formatted,
    #             "default_employee": default_employee,
    #             "default_function": default_function,
    #             "default_im_status": default_im_status,
    #             "default_industry_id": default_industry_id,
    #             "default_is_blacklisted": default_is_blacklisted,
    #             "default_is_company": default_is_company,
    #             "default_lang": default_lang,
    #             "default_message_bounce": default_message_bounce,
    #             "default_mobile": default_mobile,
    #             "default_parent_id": default_parent_id,
    #             "default_parent_name": default_parent_name,
    #             "default_partner_share": default_partner_share,
    #             "default_phone": default_phone,
    #             "default_ref": default_ref,
    #             "default_self": default_self,
    #             "default_signup_expiration": default_signup_expiration,
    #             "default_signup_token": default_signup_token,
    #             "default_signup_type": default_signup_type,
    #             "default_signup_url": default_signup_url,
    #             "default_signup_valid": default_signup_valid,
    #             "default_state_id": default_state_id,
    #             "default_street": default_street,
    #             "default_street2": default_street2,
    #             "default_supplier": default_supplier,
    #             "default_title": default_title,
    #             "default_type": default_type,
    #             "default_tz": default_tz,
    #             "default_tz_offset": default_tz_offset,
    #             "default_user_id": default_user_id,
    #             "default_vat": default_vat,
    #             "default_website": default_website,
    #             "default_zip": default_zip,
    #         },
    #     )
    #
    # @http.route(
    #     "/submitted/res_partner",
    #     type="http",
    #     auth="user",
    #     website=True,
    #     csrf=True,
    # )
    # def submit_res_partner(self, **kw):
    #     vals = {}
    #
    #     if kw.get("name"):
    #         vals["name"] = kw.get("name")
    #
    #     if kw.get("email"):
    #         vals["email"] = kw.get("email")
    #
    #     default_active = (
    #         http.request.env["res.partner"]
    #         .default_get(["active"])
    #         .get("active")
    #     )
    #     if kw.get("active"):
    #         vals["active"] = kw.get("active") == "True"
    #     elif default_active:
    #         vals["active"] = False
    #
    #     if kw.get("barcode"):
    #         vals["barcode"] = kw.get("barcode")
    #
    #     if kw.get("category_id"):
    #         lst_value_category_id = [
    #             (4, int(a))
    #             for a in request.httprequest.form.getlist("category_id")
    #         ]
    #         vals["category_id"] = lst_value_category_id
    #
    #     if kw.get("channel_ids"):
    #         lst_value_channel_ids = [
    #             (4, int(a))
    #             for a in request.httprequest.form.getlist("channel_ids")
    #         ]
    #         vals["channel_ids"] = lst_value_channel_ids
    #
    #     if kw.get("city"):
    #         vals["city"] = kw.get("city")
    #
    #     if kw.get("color"):
    #         color_value = kw.get("color")
    #         if color_value.isdigit():
    #             vals["color"] = int(color_value)
    #
    #     if kw.get("comment"):
    #         vals["comment"] = kw.get("comment")
    #
    #     if kw.get("commercial_company_name"):
    #         vals["commercial_company_name"] = kw.get("commercial_company_name")
    #
    #     if (
    #         kw.get("commercial_partner_id")
    #         and kw.get("commercial_partner_id").isdigit()
    #     ):
    #         vals["commercial_partner_id"] = int(
    #             kw.get("commercial_partner_id")
    #         )
    #
    #     if kw.get("company_id") and kw.get("company_id").isdigit():
    #         vals["company_id"] = int(kw.get("company_id"))
    #
    #     if kw.get("company_name"):
    #         vals["company_name"] = kw.get("company_name")
    #
    #     if kw.get("contact_address"):
    #         vals["contact_address"] = kw.get("contact_address")
    #
    #     if kw.get("country_id") and kw.get("country_id").isdigit():
    #         vals["country_id"] = int(kw.get("country_id"))
    #
    #     if kw.get("credit_limit"):
    #         credit_limit_value = kw.get("credit_limit")
    #         if credit_limit_value.replace(".", "", 1).isdigit():
    #             vals["credit_limit"] = float(credit_limit_value)
    #
    #     default_customer = (
    #         http.request.env["res.partner"]
    #         .default_get(["customer"])
    #         .get("customer")
    #     )
    #     if kw.get("customer"):
    #         vals["customer"] = kw.get("customer") == "True"
    #     elif default_customer:
    #         vals["customer"] = False
    #
    #     if kw.get("date"):
    #         vals["date"] = kw.get("date")
    #
    #     if kw.get("email_formatted"):
    #         vals["email_formatted"] = kw.get("email_formatted")
    #
    #     default_employee = (
    #         http.request.env["res.partner"]
    #         .default_get(["employee"])
    #         .get("employee")
    #     )
    #     if kw.get("employee"):
    #         vals["employee"] = kw.get("employee") == "True"
    #     elif default_employee:
    #         vals["employee"] = False
    #
    #     if kw.get("function"):
    #         vals["function"] = kw.get("function")
    #
    #     if kw.get("im_status"):
    #         vals["im_status"] = kw.get("im_status")
    #
    #     if kw.get("image"):
    #         lst_file_image = request.httprequest.files.getlist("image")
    #         if lst_file_image:
    #             vals["image"] = base64.b64encode(lst_file_image[-1].read())
    #
    #     if kw.get("image_medium"):
    #         lst_file_image_medium = request.httprequest.files.getlist(
    #             "image_medium"
    #         )
    #         if lst_file_image_medium:
    #             vals["image_medium"] = base64.b64encode(
    #                 lst_file_image_medium[-1].read()
    #             )
    #
    #     if kw.get("image_small"):
    #         lst_file_image_small = request.httprequest.files.getlist(
    #             "image_small"
    #         )
    #         if lst_file_image_small:
    #             vals["image_small"] = base64.b64encode(
    #                 lst_file_image_small[-1].read()
    #             )
    #
    #     if kw.get("industry_id") and kw.get("industry_id").isdigit():
    #         vals["industry_id"] = int(kw.get("industry_id"))
    #
    #     default_is_blacklisted = (
    #         http.request.env["res.partner"]
    #         .default_get(["is_blacklisted"])
    #         .get("is_blacklisted")
    #     )
    #     if kw.get("is_blacklisted"):
    #         vals["is_blacklisted"] = kw.get("is_blacklisted") == "True"
    #     elif default_is_blacklisted:
    #         vals["is_blacklisted"] = False
    #
    #     default_is_company = (
    #         http.request.env["res.partner"]
    #         .default_get(["is_company"])
    #         .get("is_company")
    #     )
    #     if kw.get("is_company"):
    #         vals["is_company"] = kw.get("is_company") == "True"
    #     elif default_is_company:
    #         vals["is_company"] = False
    #
    #     if kw.get("message_bounce"):
    #         message_bounce_value = kw.get("message_bounce")
    #         if message_bounce_value.isdigit():
    #             vals["message_bounce"] = int(message_bounce_value)
    #
    #     if kw.get("mobile"):
    #         vals["mobile"] = kw.get("mobile")
    #
    #     if kw.get("parent_id") and kw.get("parent_id").isdigit():
    #         vals["parent_id"] = int(kw.get("parent_id"))
    #
    #     if kw.get("parent_name"):
    #         vals["parent_name"] = kw.get("parent_name")
    #
    #     default_partner_share = (
    #         http.request.env["res.partner"]
    #         .default_get(["partner_share"])
    #         .get("partner_share")
    #     )
    #     if kw.get("partner_share"):
    #         vals["partner_share"] = kw.get("partner_share") == "True"
    #     elif default_partner_share:
    #         vals["partner_share"] = False
    #
    #     if kw.get("phone"):
    #         vals["phone"] = kw.get("phone")
    #
    #     if kw.get("ref"):
    #         vals["ref"] = kw.get("ref")
    #
    #     if kw.get("self") and kw.get("self").isdigit():
    #         vals["self"] = int(kw.get("self"))
    #
    #     if kw.get("signup_expiration"):
    #         vals["signup_expiration"] = kw.get("signup_expiration")
    #
    #     if kw.get("signup_token"):
    #         vals["signup_token"] = kw.get("signup_token")
    #
    #     if kw.get("signup_type"):
    #         vals["signup_type"] = kw.get("signup_type")
    #
    #     if kw.get("signup_url"):
    #         vals["signup_url"] = kw.get("signup_url")
    #
    #     default_signup_valid = (
    #         http.request.env["res.partner"]
    #         .default_get(["signup_valid"])
    #         .get("signup_valid")
    #     )
    #     if kw.get("signup_valid"):
    #         vals["signup_valid"] = kw.get("signup_valid") == "True"
    #     elif default_signup_valid:
    #         vals["signup_valid"] = False
    #
    #     if kw.get("state_id") and kw.get("state_id").isdigit():
    #         vals["state_id"] = int(kw.get("state_id"))
    #
    #     if kw.get("street"):
    #         vals["street"] = kw.get("street")
    #
    #     if kw.get("street2"):
    #         vals["street2"] = kw.get("street2")
    #
    #     default_supplier = (
    #         http.request.env["res.partner"]
    #         .default_get(["supplier"])
    #         .get("supplier")
    #     )
    #     if kw.get("supplier"):
    #         vals["supplier"] = kw.get("supplier") == "True"
    #     elif default_supplier:
    #         vals["supplier"] = False
    #
    #     if kw.get("title") and kw.get("title").isdigit():
    #         vals["title"] = int(kw.get("title"))
    #
    #     if kw.get("tz_offset"):
    #         vals["tz_offset"] = kw.get("tz_offset")
    #
    #     if kw.get("user_id") and kw.get("user_id").isdigit():
    #         vals["user_id"] = int(kw.get("user_id"))
    #
    #     if kw.get("vat"):
    #         vals["vat"] = kw.get("vat")
    #
    #     if kw.get("website"):
    #         vals["website"] = kw.get("website")
    #
    #     if kw.get("zip"):
    #         vals["zip"] = kw.get("zip")
    #
    #     new_res_partner = request.env["res.partner"].sudo().create(vals)
    #     return werkzeug.utils.redirect(f"/my/res_partner/{new_res_partner.id}")
    #
    # @http.route(
    #     "/new/ceppp_chapitre_maladie", type="http", auth="user", website=True
    # )
    # def create_new_ceppp_chapitre_maladie(self, **kw):
    #     default_nom = (
    #         http.request.env["ceppp.chapitre_maladie"]
    #         .default_get(["nom"])
    #         .get("nom")
    #     )
    #     return http.request.render(
    #         "ceppp_patient_partenaire.portal_create_ceppp_chapitre_maladie",
    #         {
    #             "page_name": "create_ceppp_chapitre_maladie",
    #             "default_nom": default_nom,
    #         },
    #     )
    #
    # @http.route(
    #     "/submitted/ceppp_chapitre_maladie",
    #     type="http",
    #     auth="user",
    #     website=True,
    #     csrf=True,
    # )
    # def submit_ceppp_chapitre_maladie(self, **kw):
    #     vals = {}
    #
    #     if kw.get("nom"):
    #         vals["nom"] = kw.get("nom")
    #
    #     new_ceppp_chapitre_maladie = (
    #         request.env["ceppp.chapitre_maladie"].sudo().create(vals)
    #     )
    #     return werkzeug.utils.redirect(
    #         f"/my/ceppp_chapitre_maladie/{new_ceppp_chapitre_maladie.id}"
    #     )
    #
    # @http.route(
    #     "/new/ceppp_competence", type="http", auth="user", website=True
    # )
    # def create_new_ceppp_competence(self, **kw):
    #     name = http.request.env.user.name
    #     return http.request.render(
    #         "ceppp_patient_partenaire.portal_create_ceppp_competence",
    #         {"name": name, "page_name": "create_ceppp_competence"},
    #     )
    #
    # @http.route(
    #     "/submitted/ceppp_competence",
    #     type="http",
    #     auth="user",
    #     website=True,
    #     csrf=True,
    # )
    # def submit_ceppp_competence(self, **kw):
    #     vals = {}
    #
    #     if kw.get("name"):
    #         vals["name"] = kw.get("name")
    #
    #     new_ceppp_competence = (
    #         request.env["ceppp.competence"].sudo().create(vals)
    #     )
    #     return werkzeug.utils.redirect(
    #         f"/my/ceppp_competence/{new_ceppp_competence.id}"
    #     )
    #
    # @http.route(
    #     "/new/ceppp_disponibilite", type="http", auth="user", website=True
    # )
    # def create_new_ceppp_disponibilite(self, **kw):
    #     name = http.request.env.user.name
    #     return http.request.render(
    #         "ceppp_patient_partenaire.portal_create_ceppp_disponibilite",
    #         {"name": name, "page_name": "create_ceppp_disponibilite"},
    #     )
    #
    # @http.route(
    #     "/submitted/ceppp_disponibilite",
    #     type="http",
    #     auth="user",
    #     website=True,
    #     csrf=True,
    # )
    # def submit_ceppp_disponibilite(self, **kw):
    #     vals = {}
    #
    #     if kw.get("name"):
    #         vals["name"] = kw.get("name")
    #
    #     new_ceppp_disponibilite = (
    #         request.env["ceppp.disponibilite"].sudo().create(vals)
    #     )
    #     return werkzeug.utils.redirect(
    #         f"/my/ceppp_disponibilite/{new_ceppp_disponibilite.id}"
    #     )

    @http.route("/new/ceppp_formation", type="http", auth="user", website=True)
    def create_new_ceppp_formation(self, **kw):
        name = http.request.env.user.name
        default_date = (
            http.request.env["ceppp.formation"]
            .default_get(["date"])
            .get("date")
        )
        default_organisation = (
            http.request.env["ceppp.formation"]
            .default_get(["organisation"])
            .get("organisation")
        )
        # recruteur_id = http.request.env["ceppp.recruteur"].search(
        #     [("active", "=", True)]
        # )
        # default_recruteur_id = (
        #     http.request.env["ceppp.formation"]
        #     .default_get(["recruteur_id"])
        #     .get("recruteur_id")
        # )
        titre_formation = http.request.env["ceppp.formation_titre"].search([])
        lst_default_titre_formation = (
            http.request.env["ceppp.formation"]
            .default_get(["titre_formation"])
            .get("titre_formation")
        )
        if lst_default_titre_formation:
            default_titre_formation = lst_default_titre_formation[0][2]
        else:
            default_titre_formation = []
        default_titre_formation_autre = (
            http.request.env["ceppp.formation"]
            .default_get(["titre_formation_autre"])
            .get("titre_formation_autre")
        )
        default_titre_formation_is_autre = (
            http.request.env["ceppp.formation"]
            .default_get(["titre_formation_is_autre"])
            .get("titre_formation_is_autre")
        )
        return http.request.render(
            "ceppp_patient_partenaire.portal_create_ceppp_formation",
            {
                "name": name,
                # "recruteur_id": recruteur_id,
                "titre_formation": titre_formation,
                "page_name": "create_ceppp_formation",
                "default_date": default_date,
                "default_organisation": default_organisation,
                # "default_recruteur_id": default_recruteur_id,
                "default_titre_formation": default_titre_formation,
                "default_titre_formation_autre": default_titre_formation_autre,
                "default_titre_formation_is_autre": default_titre_formation_is_autre,
            },
        )

    @http.route(
        "/submitted/ceppp_formation",
        type="http",
        auth="user",
        website=True,
        csrf=True,
    )
    def submit_ceppp_formation(self, **kw):
        vals = {}

        if kw.get("name"):
            vals["name"] = kw.get("name")

        if kw.get("date"):
            vals["date"] = kw.get("date")

        if kw.get("organisation"):
            vals["organisation"] = kw.get("organisation")

        # if kw.get("recruteur_id") and kw.get("recruteur_id").isdigit():
        #     vals["recruteur_id"] = int(kw.get("recruteur_id"))

        if kw.get("titre_formation"):
            lst_value_titre_formation = [
                (4, int(a))
                for a in request.httprequest.form.getlist("titre_formation")
            ]
            vals["titre_formation"] = lst_value_titre_formation

        if kw.get("titre_formation_autre"):
            vals["titre_formation_autre"] = kw.get("titre_formation_autre")

        default_titre_formation_is_autre = (
            http.request.env["ceppp.formation"]
            .default_get(["titre_formation_is_autre"])
            .get("titre_formation_is_autre")
        )
        if kw.get("titre_formation_is_autre"):
            vals["titre_formation_is_autre"] = (
                kw.get("titre_formation_is_autre") == "True"
            )
        elif default_titre_formation_is_autre:
            vals["titre_formation_is_autre"] = False

        new_ceppp_formation = (
            request.env["ceppp.formation"].sudo().create(vals)
        )
        return werkzeug.utils.redirect(
            f"/my/ceppp_formation/{new_ceppp_formation.id}"
        )

    @http.route(
        "/new/ceppp_formation_titre", type="http", auth="user", website=True
    )
    def create_new_ceppp_formation_titre(self, **kw):
        name = http.request.env.user.name
        return http.request.render(
            "ceppp_patient_partenaire.portal_create_ceppp_formation_titre",
            {"name": name, "page_name": "create_ceppp_formation_titre"},
        )

    @http.route(
        "/submitted/ceppp_formation_titre",
        type="http",
        auth="user",
        website=True,
        csrf=True,
    )
    def submit_ceppp_formation_titre(self, **kw):
        vals = {}

        if kw.get("name"):
            vals["name"] = kw.get("name")

        new_ceppp_formation_titre = (
            request.env["ceppp.formation_titre"].sudo().create(vals)
        )
        return werkzeug.utils.redirect(
            f"/my/ceppp_formation_titre/{new_ceppp_formation_titre.id}"
        )

    # @http.route(
    #     "/new/ceppp_implication", type="http", auth="user", website=True
    # )
    # def create_new_ceppp_implication(self, **kw):
    #     name = http.request.env.user.name
    #     default_description = (
    #         http.request.env["ceppp.implication"]
    #         .default_get(["description"])
    #         .get("description")
    #     )
    #     domaine = http.request.env["ceppp.implication_domaine"].search([])
    #     lst_default_domaine = (
    #         http.request.env["ceppp.implication"]
    #         .default_get(["domaine"])
    #         .get("domaine")
    #     )
    #     if lst_default_domaine:
    #         default_domaine = lst_default_domaine[0][2]
    #     else:
    #         default_domaine = []
    #     default_domaine_autre = (
    #         http.request.env["ceppp.implication"]
    #         .default_get(["domaine_autre"])
    #         .get("domaine_autre")
    #     )
    #     default_domaine_is_autre = (
    #         http.request.env["ceppp.implication"]
    #         .default_get(["domaine_is_autre"])
    #         .get("domaine_is_autre")
    #     )
    #     default_echeance_debut = (
    #         http.request.env["ceppp.implication"]
    #         .default_get(["echeance_debut"])
    #         .get("echeance_debut")
    #     )
    #     default_echeance_fin = (
    #         http.request.env["ceppp.implication"]
    #         .default_get(["echeance_fin"])
    #         .get("echeance_fin")
    #     )
    #     default_nom_equipe = (
    #         http.request.env["ceppp.implication"]
    #         .default_get(["nom_equipe"])
    #         .get("nom_equipe")
    #     )
    #     recruteur_id = http.request.env["ceppp.recruteur"].search(
    #         [("active", "=", True)]
    #     )
    #     default_recruteur_id = (
    #         http.request.env["ceppp.implication"]
    #         .default_get(["recruteur_id"])
    #         .get("recruteur_id")
    #     )
    #     role = http.request.env["ceppp.implication_role"].search([])
    #     lst_default_role = (
    #         http.request.env["ceppp.implication"]
    #         .default_get(["role"])
    #         .get("role")
    #     )
    #     if lst_default_role:
    #         default_role = lst_default_role[0][2]
    #     else:
    #         default_role = []
    #     default_role_autre = (
    #         http.request.env["ceppp.implication"]
    #         .default_get(["role_autre"])
    #         .get("role_autre")
    #     )
    #     default_role_is_autre = (
    #         http.request.env["ceppp.implication"]
    #         .default_get(["role_is_autre"])
    #         .get("role_is_autre")
    #     )
    #     default_titre = (
    #         http.request.env["ceppp.implication"]
    #         .default_get(["titre"])
    #         .get("titre")
    #     )
    #     return http.request.render(
    #         "ceppp_patient_partenaire.portal_create_ceppp_implication",
    #         {
    #             "name": name,
    #             "domaine": domaine,
    #             "recruteur_id": recruteur_id,
    #             "role": role,
    #             "page_name": "create_ceppp_implication",
    #             "default_description": default_description,
    #             "default_domaine": default_domaine,
    #             "default_domaine_autre": default_domaine_autre,
    #             "default_domaine_is_autre": default_domaine_is_autre,
    #             "default_echeance_debut": default_echeance_debut,
    #             "default_echeance_fin": default_echeance_fin,
    #             "default_nom_equipe": default_nom_equipe,
    #             "default_recruteur_id": default_recruteur_id,
    #             "default_role": default_role,
    #             "default_role_autre": default_role_autre,
    #             "default_role_is_autre": default_role_is_autre,
    #             "default_titre": default_titre,
    #         },
    #     )
    #
    # @http.route(
    #     "/submitted/ceppp_implication",
    #     type="http",
    #     auth="user",
    #     website=True,
    #     csrf=True,
    # )
    # def submit_ceppp_implication(self, **kw):
    #     vals = {}
    #
    #     if kw.get("name"):
    #         vals["name"] = kw.get("name")
    #
    #     if kw.get("description"):
    #         vals["description"] = kw.get("description")
    #
    #     if kw.get("domaine"):
    #         lst_value_domaine = [
    #             (4, int(a))
    #             for a in request.httprequest.form.getlist("domaine")
    #         ]
    #         vals["domaine"] = lst_value_domaine
    #
    #     if kw.get("domaine_autre"):
    #         vals["domaine_autre"] = kw.get("domaine_autre")
    #
    #     default_domaine_is_autre = (
    #         http.request.env["ceppp.implication"]
    #         .default_get(["domaine_is_autre"])
    #         .get("domaine_is_autre")
    #     )
    #     if kw.get("domaine_is_autre"):
    #         vals["domaine_is_autre"] = kw.get("domaine_is_autre") == "True"
    #     elif default_domaine_is_autre:
    #         vals["domaine_is_autre"] = False
    #
    #     if kw.get("echeance_debut"):
    #         vals["echeance_debut"] = kw.get("echeance_debut")
    #
    #     if kw.get("echeance_fin"):
    #         vals["echeance_fin"] = kw.get("echeance_fin")
    #
    #     if kw.get("nom_equipe"):
    #         vals["nom_equipe"] = kw.get("nom_equipe")
    #
    #     if kw.get("recruteur_id") and kw.get("recruteur_id").isdigit():
    #         vals["recruteur_id"] = int(kw.get("recruteur_id"))
    #
    #     if kw.get("role"):
    #         lst_value_role = [
    #             (4, int(a)) for a in request.httprequest.form.getlist("role")
    #         ]
    #         vals["role"] = lst_value_role
    #
    #     if kw.get("role_autre"):
    #         vals["role_autre"] = kw.get("role_autre")
    #
    #     default_role_is_autre = (
    #         http.request.env["ceppp.implication"]
    #         .default_get(["role_is_autre"])
    #         .get("role_is_autre")
    #     )
    #     if kw.get("role_is_autre"):
    #         vals["role_is_autre"] = kw.get("role_is_autre") == "True"
    #     elif default_role_is_autre:
    #         vals["role_is_autre"] = False
    #
    #     if kw.get("titre"):
    #         vals["titre"] = kw.get("titre")
    #
    #     new_ceppp_implication = (
    #         request.env["ceppp.implication"].sudo().create(vals)
    #     )
    #     return werkzeug.utils.redirect(
    #         f"/my/ceppp_implication/{new_ceppp_implication.id}"
    #     )
    #
    # @http.route(
    #     "/new/ceppp_implication_domaine",
    #     type="http",
    #     auth="user",
    #     website=True,
    # )
    # def create_new_ceppp_implication_domaine(self, **kw):
    #     name = http.request.env.user.name
    #     return http.request.render(
    #         "ceppp_patient_partenaire.portal_create_ceppp_implication_domaine",
    #         {"name": name, "page_name": "create_ceppp_implication_domaine"},
    #     )
    #
    # @http.route(
    #     "/submitted/ceppp_implication_domaine",
    #     type="http",
    #     auth="user",
    #     website=True,
    #     csrf=True,
    # )
    # def submit_ceppp_implication_domaine(self, **kw):
    #     vals = {}
    #
    #     if kw.get("name"):
    #         vals["name"] = kw.get("name")
    #
    #     new_ceppp_implication_domaine = (
    #         request.env["ceppp.implication_domaine"].sudo().create(vals)
    #     )
    #     return werkzeug.utils.redirect(
    #         f"/my/ceppp_implication_domaine/{new_ceppp_implication_domaine.id}"
    #     )
    #
    # @http.route(
    #     "/new/ceppp_implication_role", type="http", auth="user", website=True
    # )
    # def create_new_ceppp_implication_role(self, **kw):
    #     name = http.request.env.user.name
    #     return http.request.render(
    #         "ceppp_patient_partenaire.portal_create_ceppp_implication_role",
    #         {"name": name, "page_name": "create_ceppp_implication_role"},
    #     )
    #
    # @http.route(
    #     "/submitted/ceppp_implication_role",
    #     type="http",
    #     auth="user",
    #     website=True,
    #     csrf=True,
    # )
    # def submit_ceppp_implication_role(self, **kw):
    #     vals = {}
    #
    #     if kw.get("name"):
    #         vals["name"] = kw.get("name")
    #
    #     new_ceppp_implication_role = (
    #         request.env["ceppp.implication_role"].sudo().create(vals)
    #     )
    #     return werkzeug.utils.redirect(
    #         f"/my/ceppp_implication_role/{new_ceppp_implication_role.id}"
    #     )
    #
    # @http.route("/new/ceppp_langue", type="http", auth="user", website=True)
    # def create_new_ceppp_langue(self, **kw):
    #     default_nom = (
    #         http.request.env["ceppp.langue"].default_get(["nom"]).get("nom")
    #     )
    #     return http.request.render(
    #         "ceppp_patient_partenaire.portal_create_ceppp_langue",
    #         {"page_name": "create_ceppp_langue", "default_nom": default_nom},
    #     )
    #
    # @http.route(
    #     "/submitted/ceppp_langue",
    #     type="http",
    #     auth="user",
    #     website=True,
    #     csrf=True,
    # )
    # def submit_ceppp_langue(self, **kw):
    #     vals = {}
    #
    #     if kw.get("nom"):
    #         vals["nom"] = kw.get("nom")
    #
    #     new_ceppp_langue = request.env["ceppp.langue"].sudo().create(vals)
    #     return werkzeug.utils.redirect(
    #         f"/my/ceppp_langue/{new_ceppp_langue.id}"
    #     )
    #
    # @http.route("/new/ceppp_maladie", type="http", auth="user", website=True)
    # def create_new_ceppp_maladie(self, **kw):
    #     chapitre_maladie_id = http.request.env[
    #         "ceppp.chapitre_maladie"
    #     ].search([])
    #     default_chapitre_maladie_id = (
    #         http.request.env["ceppp.maladie"]
    #         .default_get(["chapitre_maladie_id"])
    #         .get("chapitre_maladie_id")
    #     )
    #     default_nom = (
    #         http.request.env["ceppp.maladie"].default_get(["nom"]).get("nom")
    #     )
    #     return http.request.render(
    #         "ceppp_patient_partenaire.portal_create_ceppp_maladie",
    #         {
    #             "chapitre_maladie_id": chapitre_maladie_id,
    #             "page_name": "create_ceppp_maladie",
    #             "default_chapitre_maladie_id": default_chapitre_maladie_id,
    #             "default_nom": default_nom,
    #         },
    #     )
    #
    # @http.route(
    #     "/submitted/ceppp_maladie",
    #     type="http",
    #     auth="user",
    #     website=True,
    #     csrf=True,
    # )
    # def submit_ceppp_maladie(self, **kw):
    #     vals = {}
    #
    #     if (
    #         kw.get("chapitre_maladie_id")
    #         and kw.get("chapitre_maladie_id").isdigit()
    #     ):
    #         vals["chapitre_maladie_id"] = int(kw.get("chapitre_maladie_id"))
    #
    #     if kw.get("nom"):
    #         vals["nom"] = kw.get("nom")
    #
    #     new_ceppp_maladie = request.env["ceppp.maladie"].sudo().create(vals)
    #     return werkzeug.utils.redirect(
    #         f"/my/ceppp_maladie/{new_ceppp_maladie.id}"
    #     )
    #
    # @http.route(
    #     "/new/ceppp_maladie_proche_aidant",
    #     type="http",
    #     auth="user",
    #     website=True,
    # )
    # def create_new_ceppp_maladie_proche_aidant(self, **kw):
    #     name = http.request.env.user.name
    #     maladie = http.request.env["ceppp.maladie"].search([])
    #     lst_default_maladie = (
    #         http.request.env["ceppp.maladie_proche_aidant"]
    #         .default_get(["maladie"])
    #         .get("maladie")
    #     )
    #     if lst_default_maladie:
    #         default_maladie = lst_default_maladie[0][2]
    #     else:
    #         default_maladie = []
    #     recruteur_id = http.request.env["ceppp.recruteur"].search(
    #         [("active", "=", True)]
    #     )
    #     default_recruteur_id = (
    #         http.request.env["ceppp.maladie_proche_aidant"]
    #         .default_get(["recruteur_id"])
    #         .get("recruteur_id")
    #     )
    #     relation = http.request.env["ceppp.relation_proche"].search([])
    #     lst_default_relation = (
    #         http.request.env["ceppp.maladie_proche_aidant"]
    #         .default_get(["relation"])
    #         .get("relation")
    #     )
    #     if lst_default_relation:
    #         default_relation = lst_default_relation[0][2]
    #     else:
    #         default_relation = []
    #     default_relation_autre = (
    #         http.request.env["ceppp.maladie_proche_aidant"]
    #         .default_get(["relation_autre"])
    #         .get("relation_autre")
    #     )
    #     default_relation_is_autre = (
    #         http.request.env["ceppp.maladie_proche_aidant"]
    #         .default_get(["relation_is_autre"])
    #         .get("relation_is_autre")
    #     )
    #     return http.request.render(
    #         "ceppp_patient_partenaire.portal_create_ceppp_maladie_proche_aidant",
    #         {
    #             "name": name,
    #             "maladie": maladie,
    #             "recruteur_id": recruteur_id,
    #             "relation": relation,
    #             "page_name": "create_ceppp_maladie_proche_aidant",
    #             "default_maladie": default_maladie,
    #             "default_recruteur_id": default_recruteur_id,
    #             "default_relation": default_relation,
    #             "default_relation_autre": default_relation_autre,
    #             "default_relation_is_autre": default_relation_is_autre,
    #         },
    #     )
    #
    # @http.route(
    #     "/submitted/ceppp_maladie_proche_aidant",
    #     type="http",
    #     auth="user",
    #     website=True,
    #     csrf=True,
    # )
    # def submit_ceppp_maladie_proche_aidant(self, **kw):
    #     vals = {}
    #
    #     if kw.get("name"):
    #         vals["name"] = kw.get("name")
    #
    #     if kw.get("maladie"):
    #         lst_value_maladie = [
    #             (4, int(a))
    #             for a in request.httprequest.form.getlist("maladie")
    #         ]
    #         vals["maladie"] = lst_value_maladie
    #
    #     if kw.get("recruteur_id") and kw.get("recruteur_id").isdigit():
    #         vals["recruteur_id"] = int(kw.get("recruteur_id"))
    #
    #     if kw.get("relation"):
    #         lst_value_relation = [
    #             (4, int(a))
    #             for a in request.httprequest.form.getlist("relation")
    #         ]
    #         vals["relation"] = lst_value_relation
    #
    #     if kw.get("relation_autre"):
    #         vals["relation_autre"] = kw.get("relation_autre")
    #
    #     default_relation_is_autre = (
    #         http.request.env["ceppp.maladie_proche_aidant"]
    #         .default_get(["relation_is_autre"])
    #         .get("relation_is_autre")
    #     )
    #     if kw.get("relation_is_autre"):
    #         vals["relation_is_autre"] = kw.get("relation_is_autre") == "True"
    #     elif default_relation_is_autre:
    #         vals["relation_is_autre"] = False
    #
    #     new_ceppp_maladie_proche_aidant = (
    #         request.env["ceppp.maladie_proche_aidant"].sudo().create(vals)
    #     )
    #     return werkzeug.utils.redirect(
    #         f"/my/ceppp_maladie_proche_aidant/{new_ceppp_maladie_proche_aidant.id}"
    #     )
    #
    # @http.route(
    #     "/new/ceppp_mode_communication_privilegie",
    #     type="http",
    #     auth="user",
    #     website=True,
    # )
    # def create_new_ceppp_mode_communication_privilegie(self, **kw):
    #     name = http.request.env.user.name
    #     return http.request.render(
    #         "ceppp_patient_partenaire.portal_create_ceppp_mode_communication_privilegie",
    #         {
    #             "name": name,
    #             "page_name": "create_ceppp_mode_communication_privilegie",
    #         },
    #     )
    #
    # @http.route(
    #     "/submitted/ceppp_mode_communication_privilegie",
    #     type="http",
    #     auth="user",
    #     website=True,
    #     csrf=True,
    # )
    # def submit_ceppp_mode_communication_privilegie(self, **kw):
    #     vals = {}
    #
    #     if kw.get("name"):
    #         vals["name"] = kw.get("name")
    #
    #     new_ceppp_mode_communication_privilegie = (
    #         request.env["ceppp.mode_communication_privilegie"]
    #         .sudo()
    #         .create(vals)
    #     )
    #     return werkzeug.utils.redirect(
    #         f"/my/ceppp_mode_communication_privilegie/{new_ceppp_mode_communication_privilegie.id}"
    #     )
    #
    # @http.route(
    #     "/new/ceppp_occupation", type="http", auth="user", website=True
    # )
    # def create_new_ceppp_occupation(self, **kw):
    #     name = http.request.env.user.name
    #     return http.request.render(
    #         "ceppp_patient_partenaire.portal_create_ceppp_occupation",
    #         {"name": name, "page_name": "create_ceppp_occupation"},
    #     )
    #
    # @http.route(
    #     "/submitted/ceppp_occupation",
    #     type="http",
    #     auth="user",
    #     website=True,
    #     csrf=True,
    # )
    # def submit_ceppp_occupation(self, **kw):
    #     vals = {}
    #
    #     if kw.get("name"):
    #         vals["name"] = kw.get("name")
    #
    #     new_ceppp_occupation = (
    #         request.env["ceppp.occupation"].sudo().create(vals)
    #     )
    #     return werkzeug.utils.redirect(
    #         f"/my/ceppp_occupation/{new_ceppp_occupation.id}"
    #     )
    #
    # @http.route("/new/ceppp_patient", type="http", auth="user", website=True)
    # def create_new_ceppp_patient(self, **kw):
    #     name = http.request.env.user.name
    #     default_centre_recruteur = (
    #         http.request.env["ceppp.patient"]
    #         .default_get(["centre_recruteur"])
    #         .get("centre_recruteur")
    #     )
    #     default_consentement_notification = (
    #         http.request.env["ceppp.patient"]
    #         .default_get(["consentement_notification"])
    #         .get("consentement_notification")
    #     )
    #     default_consentement_recherche = (
    #         http.request.env["ceppp.patient"]
    #         .default_get(["consentement_recherche"])
    #         .get("consentement_recherche")
    #     )
    #     default_consentement_recrutement = (
    #         http.request.env["ceppp.patient"]
    #         .default_get(["consentement_recrutement"])
    #         .get("consentement_recrutement")
    #     )
    #     disponibilite = http.request.env["ceppp.disponibilite"].search([])
    #     lst_default_disponibilite = (
    #         http.request.env["ceppp.patient"]
    #         .default_get(["disponibilite"])
    #         .get("disponibilite")
    #     )
    #     if lst_default_disponibilite:
    #         default_disponibilite = lst_default_disponibilite[0][2]
    #     else:
    #         default_disponibilite = []
    #     disponibilite_not = http.request.env["ceppp.disponibilite"].search([])
    #     lst_default_disponibilite_not = (
    #         http.request.env["ceppp.patient"]
    #         .default_get(["disponibilite_not"])
    #         .get("disponibilite_not")
    #     )
    #     if lst_default_disponibilite_not:
    #         default_disponibilite_not = lst_default_disponibilite_not[0][2]
    #     else:
    #         default_disponibilite_not = []
    #     maladie_soi_meme = http.request.env["ceppp.maladie"].search([])
    #     lst_default_maladie_soi_meme = (
    #         http.request.env["ceppp.patient"]
    #         .default_get(["maladie_soi_meme"])
    #         .get("maladie_soi_meme")
    #     )
    #     if lst_default_maladie_soi_meme:
    #         default_maladie_soi_meme = lst_default_maladie_soi_meme[0][2]
    #     else:
    #         default_maladie_soi_meme = []
    #     recruteur_id = http.request.env["ceppp.recruteur"].search(
    #         [("active", "=", True)]
    #     )
    #     default_recruteur_id = (
    #         http.request.env["ceppp.patient"]
    #         .default_get(["recruteur_id"])
    #         .get("recruteur_id")
    #     )
    #     recruteur_partner_id = http.request.env["res.partner"].search(
    #         [("active", "=", True)]
    #     )
    #     default_recruteur_partner_id = (
    #         http.request.env["ceppp.patient"]
    #         .default_get(["recruteur_partner_id"])
    #         .get("recruteur_partner_id")
    #     )
    #     default_uuid = (
    #         http.request.env["ceppp.patient"].default_get(["uuid"]).get("uuid")
    #     )
    #     return http.request.render(
    #         "ceppp_patient_partenaire.portal_create_ceppp_patient",
    #         {
    #             "name": name,
    #             "disponibilite": disponibilite,
    #             "disponibilite_not": disponibilite_not,
    #             "maladie_soi_meme": maladie_soi_meme,
    #             "recruteur_id": recruteur_id,
    #             "recruteur_partner_id": recruteur_partner_id,
    #             "page_name": "create_ceppp_patient",
    #             "default_centre_recruteur": default_centre_recruteur,
    #             "default_consentement_notification": default_consentement_notification,
    #             "default_consentement_recherche": default_consentement_recherche,
    #             "default_consentement_recrutement": default_consentement_recrutement,
    #             "default_disponibilite": default_disponibilite,
    #             "default_disponibilite_not": default_disponibilite_not,
    #             "default_maladie_soi_meme": default_maladie_soi_meme,
    #             "default_recruteur_id": default_recruteur_id,
    #             "default_recruteur_partner_id": default_recruteur_partner_id,
    #             "default_uuid": default_uuid,
    #         },
    #     )
    #
    # @http.route(
    #     "/submitted/ceppp_patient",
    #     type="http",
    #     auth="user",
    #     website=True,
    #     csrf=True,
    # )
    # def submit_ceppp_patient(self, **kw):
    #     vals = {}
    #
    #     if kw.get("name"):
    #         vals["name"] = kw.get("name")
    #
    #     if kw.get("centre_recruteur"):
    #         vals["centre_recruteur"] = kw.get("centre_recruteur")
    #
    #     default_consentement_notification = (
    #         http.request.env["ceppp.patient"]
    #         .default_get(["consentement_notification"])
    #         .get("consentement_notification")
    #     )
    #     if kw.get("consentement_notification"):
    #         vals["consentement_notification"] = (
    #             kw.get("consentement_notification") == "True"
    #         )
    #     elif default_consentement_notification:
    #         vals["consentement_notification"] = False
    #
    #     default_consentement_recherche = (
    #         http.request.env["ceppp.patient"]
    #         .default_get(["consentement_recherche"])
    #         .get("consentement_recherche")
    #     )
    #     if kw.get("consentement_recherche"):
    #         vals["consentement_recherche"] = (
    #             kw.get("consentement_recherche") == "True"
    #         )
    #     elif default_consentement_recherche:
    #         vals["consentement_recherche"] = False
    #
    #     default_consentement_recrutement = (
    #         http.request.env["ceppp.patient"]
    #         .default_get(["consentement_recrutement"])
    #         .get("consentement_recrutement")
    #     )
    #     if kw.get("consentement_recrutement"):
    #         vals["consentement_recrutement"] = (
    #             kw.get("consentement_recrutement") == "True"
    #         )
    #     elif default_consentement_recrutement:
    #         vals["consentement_recrutement"] = False
    #
    #     if kw.get("disponibilite"):
    #         lst_value_disponibilite = [
    #             (4, int(a))
    #             for a in request.httprequest.form.getlist("disponibilite")
    #         ]
    #         vals["disponibilite"] = lst_value_disponibilite
    #
    #     if kw.get("disponibilite_not"):
    #         lst_value_disponibilite_not = [
    #             (4, int(a))
    #             for a in request.httprequest.form.getlist("disponibilite_not")
    #         ]
    #         vals["disponibilite_not"] = lst_value_disponibilite_not
    #
    #     if kw.get("maladie_soi_meme"):
    #         lst_value_maladie_soi_meme = [
    #             (4, int(a))
    #             for a in request.httprequest.form.getlist("maladie_soi_meme")
    #         ]
    #         vals["maladie_soi_meme"] = lst_value_maladie_soi_meme
    #
    #     if kw.get("recruteur_id") and kw.get("recruteur_id").isdigit():
    #         vals["recruteur_id"] = int(kw.get("recruteur_id"))
    #
    #     if (
    #         kw.get("recruteur_partner_id")
    #         and kw.get("recruteur_partner_id").isdigit()
    #     ):
    #         vals["recruteur_partner_id"] = int(kw.get("recruteur_partner_id"))
    #
    #     if kw.get("uuid"):
    #         vals["uuid"] = kw.get("uuid")
    #
    #     new_ceppp_patient = request.env["ceppp.patient"].sudo().create(vals)
    #     return werkzeug.utils.redirect(
    #         f"/my/ceppp_patient/{new_ceppp_patient.id}"
    #     )
    #
    # @http.route("/new/ceppp_recruteur", type="http", auth="user", website=True)
    # def create_new_ceppp_recruteur(self, **kw):
    #     name = http.request.env.user.name
    #     default_active = (
    #         http.request.env["ceppp.recruteur"]
    #         .default_get(["active"])
    #         .get("active")
    #     )
    #     default_adresse_postale = (
    #         http.request.env["ceppp.recruteur"]
    #         .default_get(["adresse_postale"])
    #         .get("adresse_postale")
    #     )
    #     default_centre_recruteur = (
    #         http.request.env["ceppp.recruteur"]
    #         .default_get(["centre_recruteur"])
    #         .get("centre_recruteur")
    #     )
    #     default_commentaires = (
    #         http.request.env["ceppp.recruteur"]
    #         .default_get(["commentaires"])
    #         .get("commentaires")
    #     )
    #     competence_patient = http.request.env["ceppp.competence"].search([])
    #     lst_default_competence_patient = (
    #         http.request.env["ceppp.recruteur"]
    #         .default_get(["competence_patient"])
    #         .get("competence_patient")
    #     )
    #     if lst_default_competence_patient:
    #         default_competence_patient = lst_default_competence_patient[0][2]
    #     else:
    #         default_competence_patient = []
    #     default_consentement_notification = (
    #         http.request.env["ceppp.recruteur"]
    #         .default_get(["consentement_notification"])
    #         .get("consentement_notification")
    #     )
    #     default_consentement_recherche = (
    #         http.request.env["ceppp.recruteur"]
    #         .default_get(["consentement_recherche"])
    #         .get("consentement_recherche")
    #     )
    #     default_consentement_recrutement = (
    #         http.request.env["ceppp.recruteur"]
    #         .default_get(["consentement_recrutement"])
    #         .get("consentement_recrutement")
    #     )
    #     default_courriel = (
    #         http.request.env["ceppp.recruteur"]
    #         .default_get(["courriel"])
    #         .get("courriel")
    #     )
    #     default_date_naissance = (
    #         http.request.env["ceppp.recruteur"]
    #         .default_get(["date_naissance"])
    #         .get("date_naissance")
    #     )
    #     disponibilite = http.request.env["ceppp.disponibilite"].search([])
    #     lst_default_disponibilite = (
    #         http.request.env["ceppp.recruteur"]
    #         .default_get(["disponibilite"])
    #         .get("disponibilite")
    #     )
    #     if lst_default_disponibilite:
    #         default_disponibilite = lst_default_disponibilite[0][2]
    #     else:
    #         default_disponibilite = []
    #     disponibilite_not = http.request.env["ceppp.disponibilite"].search([])
    #     lst_default_disponibilite_not = (
    #         http.request.env["ceppp.recruteur"]
    #         .default_get(["disponibilite_not"])
    #         .get("disponibilite_not")
    #     )
    #     if lst_default_disponibilite_not:
    #         default_disponibilite_not = lst_default_disponibilite_not[0][2]
    #     else:
    #         default_disponibilite_not = []
    #     default_formation_professionnelle = (
    #         http.request.env["ceppp.recruteur"]
    #         .default_get(["formation_professionnelle"])
    #         .get("formation_professionnelle")
    #     )
    #     genre = http.request.env["ceppp.recruteur"]._fields["genre"].selection
    #     default_genre = (
    #         http.request.env["ceppp.recruteur"]
    #         .default_get(["genre"])
    #         .get("genre")
    #     )
    #     default_genre_autre = (
    #         http.request.env["ceppp.recruteur"]
    #         .default_get(["genre_autre"])
    #         .get("genre_autre")
    #     )
    #     heritage_culturel = (
    #         http.request.env["ceppp.recruteur"]
    #         ._fields["heritage_culturel"]
    #         .selection
    #     )
    #     default_heritage_culturel = (
    #         http.request.env["ceppp.recruteur"]
    #         .default_get(["heritage_culturel"])
    #         .get("heritage_culturel")
    #     )
    #     default_langue_is_autre = (
    #         http.request.env["ceppp.recruteur"]
    #         .default_get(["langue_is_autre"])
    #         .get("langue_is_autre")
    #     )
    #     langue_parle_ecrit = http.request.env["ceppp.langue"].search([])
    #     lst_default_langue_parle_ecrit = (
    #         http.request.env["ceppp.recruteur"]
    #         .default_get(["langue_parle_ecrit"])
    #         .get("langue_parle_ecrit")
    #     )
    #     if lst_default_langue_parle_ecrit:
    #         default_langue_parle_ecrit = lst_default_langue_parle_ecrit[0][2]
    #     else:
    #         default_langue_parle_ecrit = []
    #     default_langue_parle_ecrit_autre = (
    #         http.request.env["ceppp.recruteur"]
    #         .default_get(["langue_parle_ecrit_autre"])
    #         .get("langue_parle_ecrit_autre")
    #     )
    #     maladie_soi_meme = http.request.env["ceppp.maladie"].search([])
    #     lst_default_maladie_soi_meme = (
    #         http.request.env["ceppp.recruteur"]
    #         .default_get(["maladie_soi_meme"])
    #         .get("maladie_soi_meme")
    #     )
    #     if lst_default_maladie_soi_meme:
    #         default_maladie_soi_meme = lst_default_maladie_soi_meme[0][2]
    #     else:
    #         default_maladie_soi_meme = []
    #     default_mobile = (
    #         http.request.env["ceppp.recruteur"]
    #         .default_get(["mobile"])
    #         .get("mobile")
    #     )
    #     mode_communication_privilegie = http.request.env[
    #         "ceppp.mode_communication_privilegie"
    #     ].search([])
    #     lst_default_mode_communication_privilegie = (
    #         http.request.env["ceppp.recruteur"]
    #         .default_get(["mode_communication_privilegie"])
    #         .get("mode_communication_privilegie")
    #     )
    #     if lst_default_mode_communication_privilegie:
    #         default_mode_communication_privilegie = (
    #             lst_default_mode_communication_privilegie[0][2]
    #         )
    #     else:
    #         default_mode_communication_privilegie = []
    #     occupation = http.request.env["ceppp.occupation"].search([])
    #     lst_default_occupation = (
    #         http.request.env["ceppp.recruteur"]
    #         .default_get(["occupation"])
    #         .get("occupation")
    #     )
    #     if lst_default_occupation:
    #         default_occupation = lst_default_occupation[0][2]
    #     else:
    #         default_occupation = []
    #     default_occupation_autre = (
    #         http.request.env["ceppp.recruteur"]
    #         .default_get(["occupation_autre"])
    #         .get("occupation_autre")
    #     )
    #     default_occupation_is_autre = (
    #         http.request.env["ceppp.recruteur"]
    #         .default_get(["occupation_is_autre"])
    #         .get("occupation_is_autre")
    #     )
    #     patient_actif = (
    #         http.request.env["ceppp.recruteur"]
    #         ._fields["patient_actif"]
    #         .selection
    #     )
    #     default_patient_actif = (
    #         http.request.env["ceppp.recruteur"]
    #         .default_get(["patient_actif"])
    #         .get("patient_actif")
    #     )
    #     patient_partner_id = http.request.env["res.partner"].search(
    #         [("active", "=", True)]
    #     )
    #     default_patient_partner_id = (
    #         http.request.env["ceppp.recruteur"]
    #         .default_get(["patient_partner_id"])
    #         .get("patient_partner_id")
    #     )
    #     recruteur_partner_id = http.request.env["res.partner"].search(
    #         [("active", "=", True)]
    #     )
    #     default_recruteur_partner_id = (
    #         http.request.env["ceppp.recruteur"]
    #         .default_get(["recruteur_partner_id"])
    #         .get("recruteur_partner_id")
    #     )
    #     recruteur_user_id = http.request.env["res.users"].search(
    #         [("active", "=", True)]
    #     )
    #     default_recruteur_user_id = (
    #         http.request.env["ceppp.recruteur"]
    #         .default_get(["recruteur_user_id"])
    #         .get("recruteur_user_id")
    #     )
    #     sexe = http.request.env["ceppp.recruteur"]._fields["sexe"].selection
    #     default_sexe = (
    #         http.request.env["ceppp.recruteur"]
    #         .default_get(["sexe"])
    #         .get("sexe")
    #     )
    #     default_telephone = (
    #         http.request.env["ceppp.recruteur"]
    #         .default_get(["telephone"])
    #         .get("telephone")
    #     )
    #     default_user_is_admin = (
    #         http.request.env["ceppp.recruteur"]
    #         .default_get(["user_is_admin"])
    #         .get("user_is_admin")
    #     )
    #     default_uuid = (
    #         http.request.env["ceppp.recruteur"]
    #         .default_get(["uuid"])
    #         .get("uuid")
    #     )
    #     return http.request.render(
    #         "ceppp_patient_partenaire.portal_create_ceppp_recruteur",
    #         {
    #             "name": name,
    #             "competence_patient": competence_patient,
    #             "disponibilite": disponibilite,
    #             "disponibilite_not": disponibilite_not,
    #             "genre": genre,
    #             "heritage_culturel": heritage_culturel,
    #             "langue_parle_ecrit": langue_parle_ecrit,
    #             "maladie_soi_meme": maladie_soi_meme,
    #             "mode_communication_privilegie": mode_communication_privilegie,
    #             "occupation": occupation,
    #             "patient_actif": patient_actif,
    #             "patient_partner_id": patient_partner_id,
    #             "recruteur_partner_id": recruteur_partner_id,
    #             "recruteur_user_id": recruteur_user_id,
    #             "sexe": sexe,
    #             "page_name": "create_ceppp_recruteur",
    #             "default_active": default_active,
    #             "default_adresse_postale": default_adresse_postale,
    #             "default_centre_recruteur": default_centre_recruteur,
    #             "default_commentaires": default_commentaires,
    #             "default_competence_patient": default_competence_patient,
    #             "default_consentement_notification": default_consentement_notification,
    #             "default_consentement_recherche": default_consentement_recherche,
    #             "default_consentement_recrutement": default_consentement_recrutement,
    #             "default_courriel": default_courriel,
    #             "default_date_naissance": default_date_naissance,
    #             "default_disponibilite": default_disponibilite,
    #             "default_disponibilite_not": default_disponibilite_not,
    #             "default_formation_professionnelle": default_formation_professionnelle,
    #             "default_genre": default_genre,
    #             "default_genre_autre": default_genre_autre,
    #             "default_heritage_culturel": default_heritage_culturel,
    #             "default_langue_is_autre": default_langue_is_autre,
    #             "default_langue_parle_ecrit": default_langue_parle_ecrit,
    #             "default_langue_parle_ecrit_autre": default_langue_parle_ecrit_autre,
    #             "default_maladie_soi_meme": default_maladie_soi_meme,
    #             "default_mobile": default_mobile,
    #             "default_mode_communication_privilegie": default_mode_communication_privilegie,
    #             "default_occupation": default_occupation,
    #             "default_occupation_autre": default_occupation_autre,
    #             "default_occupation_is_autre": default_occupation_is_autre,
    #             "default_patient_actif": default_patient_actif,
    #             "default_patient_partner_id": default_patient_partner_id,
    #             "default_recruteur_partner_id": default_recruteur_partner_id,
    #             "default_recruteur_user_id": default_recruteur_user_id,
    #             "default_sexe": default_sexe,
    #             "default_telephone": default_telephone,
    #             "default_user_is_admin": default_user_is_admin,
    #             "default_uuid": default_uuid,
    #         },
    #     )
    #
    # @http.route(
    #     "/submitted/ceppp_recruteur",
    #     type="http",
    #     auth="user",
    #     website=True,
    #     csrf=True,
    # )
    # def submit_ceppp_recruteur(self, **kw):
    #     vals = {}
    #
    #     if kw.get("name"):
    #         vals["name"] = kw.get("name")
    #
    #     default_active = (
    #         http.request.env["ceppp.recruteur"]
    #         .default_get(["active"])
    #         .get("active")
    #     )
    #     if kw.get("active"):
    #         vals["active"] = kw.get("active") == "True"
    #     elif default_active:
    #         vals["active"] = False
    #
    #     if kw.get("adresse_postale"):
    #         vals["adresse_postale"] = kw.get("adresse_postale")
    #
    #     if kw.get("centre_recruteur"):
    #         vals["centre_recruteur"] = kw.get("centre_recruteur")
    #
    #     if kw.get("commentaires"):
    #         vals["commentaires"] = kw.get("commentaires")
    #
    #     if kw.get("competence_patient"):
    #         lst_value_competence_patient = [
    #             (4, int(a))
    #             for a in request.httprequest.form.getlist("competence_patient")
    #         ]
    #         vals["competence_patient"] = lst_value_competence_patient
    #
    #     default_consentement_notification = (
    #         http.request.env["ceppp.recruteur"]
    #         .default_get(["consentement_notification"])
    #         .get("consentement_notification")
    #     )
    #     if kw.get("consentement_notification"):
    #         vals["consentement_notification"] = (
    #             kw.get("consentement_notification") == "True"
    #         )
    #     elif default_consentement_notification:
    #         vals["consentement_notification"] = False
    #
    #     default_consentement_recherche = (
    #         http.request.env["ceppp.recruteur"]
    #         .default_get(["consentement_recherche"])
    #         .get("consentement_recherche")
    #     )
    #     if kw.get("consentement_recherche"):
    #         vals["consentement_recherche"] = (
    #             kw.get("consentement_recherche") == "True"
    #         )
    #     elif default_consentement_recherche:
    #         vals["consentement_recherche"] = False
    #
    #     default_consentement_recrutement = (
    #         http.request.env["ceppp.recruteur"]
    #         .default_get(["consentement_recrutement"])
    #         .get("consentement_recrutement")
    #     )
    #     if kw.get("consentement_recrutement"):
    #         vals["consentement_recrutement"] = (
    #             kw.get("consentement_recrutement") == "True"
    #         )
    #     elif default_consentement_recrutement:
    #         vals["consentement_recrutement"] = False
    #
    #     if kw.get("courriel"):
    #         vals["courriel"] = kw.get("courriel")
    #
    #     if kw.get("date_naissance"):
    #         vals["date_naissance"] = kw.get("date_naissance")
    #
    #     if kw.get("disponibilite"):
    #         lst_value_disponibilite = [
    #             (4, int(a))
    #             for a in request.httprequest.form.getlist("disponibilite")
    #         ]
    #         vals["disponibilite"] = lst_value_disponibilite
    #
    #     if kw.get("disponibilite_not"):
    #         lst_value_disponibilite_not = [
    #             (4, int(a))
    #             for a in request.httprequest.form.getlist("disponibilite_not")
    #         ]
    #         vals["disponibilite_not"] = lst_value_disponibilite_not
    #
    #     if kw.get("formation_professionnelle"):
    #         vals["formation_professionnelle"] = kw.get(
    #             "formation_professionnelle"
    #         )
    #
    #     if kw.get("genre_autre"):
    #         vals["genre_autre"] = kw.get("genre_autre")
    #
    #     if kw.get("image"):
    #         lst_file_image = request.httprequest.files.getlist("image")
    #         if lst_file_image:
    #             vals["image"] = base64.b64encode(lst_file_image[-1].read())
    #
    #     if kw.get("image_medium"):
    #         lst_file_image_medium = request.httprequest.files.getlist(
    #             "image_medium"
    #         )
    #         if lst_file_image_medium:
    #             vals["image_medium"] = base64.b64encode(
    #                 lst_file_image_medium[-1].read()
    #             )
    #
    #     if kw.get("image_small"):
    #         lst_file_image_small = request.httprequest.files.getlist(
    #             "image_small"
    #         )
    #         if lst_file_image_small:
    #             vals["image_small"] = base64.b64encode(
    #                 lst_file_image_small[-1].read()
    #             )
    #
    #     default_langue_is_autre = (
    #         http.request.env["ceppp.recruteur"]
    #         .default_get(["langue_is_autre"])
    #         .get("langue_is_autre")
    #     )
    #     if kw.get("langue_is_autre"):
    #         vals["langue_is_autre"] = kw.get("langue_is_autre") == "True"
    #     elif default_langue_is_autre:
    #         vals["langue_is_autre"] = False
    #
    #     if kw.get("langue_parle_ecrit"):
    #         lst_value_langue_parle_ecrit = [
    #             (4, int(a))
    #             for a in request.httprequest.form.getlist("langue_parle_ecrit")
    #         ]
    #         vals["langue_parle_ecrit"] = lst_value_langue_parle_ecrit
    #
    #     if kw.get("langue_parle_ecrit_autre"):
    #         vals["langue_parle_ecrit_autre"] = kw.get(
    #             "langue_parle_ecrit_autre"
    #         )
    #
    #     if kw.get("maladie_soi_meme"):
    #         lst_value_maladie_soi_meme = [
    #             (4, int(a))
    #             for a in request.httprequest.form.getlist("maladie_soi_meme")
    #         ]
    #         vals["maladie_soi_meme"] = lst_value_maladie_soi_meme
    #
    #     if kw.get("mobile"):
    #         vals["mobile"] = kw.get("mobile")
    #
    #     if kw.get("mode_communication_privilegie"):
    #         lst_value_mode_communication_privilegie = [
    #             (4, int(a))
    #             for a in request.httprequest.form.getlist(
    #                 "mode_communication_privilegie"
    #             )
    #         ]
    #         vals[
    #             "mode_communication_privilegie"
    #         ] = lst_value_mode_communication_privilegie
    #
    #     if kw.get("occupation"):
    #         lst_value_occupation = [
    #             (4, int(a))
    #             for a in request.httprequest.form.getlist("occupation")
    #         ]
    #         vals["occupation"] = lst_value_occupation
    #
    #     if kw.get("occupation_autre"):
    #         vals["occupation_autre"] = kw.get("occupation_autre")
    #
    #     default_occupation_is_autre = (
    #         http.request.env["ceppp.recruteur"]
    #         .default_get(["occupation_is_autre"])
    #         .get("occupation_is_autre")
    #     )
    #     if kw.get("occupation_is_autre"):
    #         vals["occupation_is_autre"] = (
    #             kw.get("occupation_is_autre") == "True"
    #         )
    #     elif default_occupation_is_autre:
    #         vals["occupation_is_autre"] = False
    #
    #     if (
    #         kw.get("patient_partner_id")
    #         and kw.get("patient_partner_id").isdigit()
    #     ):
    #         vals["patient_partner_id"] = int(kw.get("patient_partner_id"))
    #
    #     if (
    #         kw.get("recruteur_partner_id")
    #         and kw.get("recruteur_partner_id").isdigit()
    #     ):
    #         vals["recruteur_partner_id"] = int(kw.get("recruteur_partner_id"))
    #
    #     if (
    #         kw.get("recruteur_user_id")
    #         and kw.get("recruteur_user_id").isdigit()
    #     ):
    #         vals["recruteur_user_id"] = int(kw.get("recruteur_user_id"))
    #
    #     if kw.get("telephone"):
    #         vals["telephone"] = kw.get("telephone")
    #
    #     default_user_is_admin = (
    #         http.request.env["ceppp.recruteur"]
    #         .default_get(["user_is_admin"])
    #         .get("user_is_admin")
    #     )
    #     if kw.get("user_is_admin"):
    #         vals["user_is_admin"] = kw.get("user_is_admin") == "True"
    #     elif default_user_is_admin:
    #         vals["user_is_admin"] = False
    #
    #     if kw.get("uuid"):
    #         vals["uuid"] = kw.get("uuid")
    #
    #     new_ceppp_recruteur = (
    #         request.env["ceppp.recruteur"].sudo().create(vals)
    #     )
    #     return werkzeug.utils.redirect(
    #         f"/my/ceppp_recruteur/{new_ceppp_recruteur.id}"
    #     )
    #
    # @http.route(
    #     "/new/ceppp_relation_proche", type="http", auth="user", website=True
    # )
    # def create_new_ceppp_relation_proche(self, **kw):
    #     name = http.request.env.user.name
    #     return http.request.render(
    #         "ceppp_patient_partenaire.portal_create_ceppp_relation_proche",
    #         {"name": name, "page_name": "create_ceppp_relation_proche"},
    #     )
    #
    # @http.route(
    #     "/submitted/ceppp_relation_proche",
    #     type="http",
    #     auth="user",
    #     website=True,
    #     csrf=True,
    # )
    # def submit_ceppp_relation_proche(self, **kw):
    #     vals = {}
    #
    #     if kw.get("name"):
    #         vals["name"] = kw.get("name")
    #
    #     new_ceppp_relation_proche = (
    #         request.env["ceppp.relation_proche"].sudo().create(vals)
    #     )
    #     return werkzeug.utils.redirect(
    #         f"/my/ceppp_relation_proche/{new_ceppp_relation_proche.id}"
    #     )
