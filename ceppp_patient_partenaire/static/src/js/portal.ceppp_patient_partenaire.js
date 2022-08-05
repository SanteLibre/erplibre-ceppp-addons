odoo.define(
    "ceppp_patient_partenaire.ceppp_patient_partenaire_portal",
    function (require) {
        "use strict";

        require("web.dom_ready");
        let time = require("web.time");
        let ajax = require("web.ajax");
        let base = require("web_editor.base");
        let context = require("web_editor.context");

        // Support autre rôle
        $('#div_autre_role').hide();

        $("input[id^='role_Autre_']").on("click", function (event) {
            // event.preventDefault();
            let n = $("input[id^='role_Autre_']:checked").length;
            if (n > 0) {
                $('#div_autre_role').show();
            } else {
                $('#div_autre_role').hide();
            }
        });

        // Support autre domaine
        $('#div_autre_domaine').hide();

        $("input[id^='domaine_Autre_']").on("click", function (event) {
            // event.preventDefault();
            let n = $("input[id^='domaine_Autre_']:checked").length;
            if (n > 0) {
                $('#div_autre_domaine').show();
            } else {
                $('#div_autre_domaine').hide();
            }
        });

        // Support autre relation
        $('#div_autre_relation').hide();

        $("input[id^='relation_Autre_']").on("click", function (event) {
            // event.preventDefault();
            let n = $("input[id^='relation_Autre_']:checked").length;
            if (n > 0) {
                $('#div_autre_relation').show();
            } else {
                $('#div_autre_relation').hide();
            }
        });

        // Support autre formation
        $('#div_autre_formation').hide();

        $("input[id^='titre_formation_Autre_']").on("click", function (event) {
            // event.preventDefault();
            let n = $("input[id^='titre_formation_Autre_']:checked").length;
            if (n > 0) {
                $('#div_autre_formation').show();
            } else {
                $('#div_autre_formation').hide();
            }
        });

        function load_locale() {
            let url = "/web/webclient/locale/" + context.get().lang || "en_US";
            return ajax.loadJS(url);
        }

        let ready_with_locale = $.when(base.ready(), load_locale());
        ready_with_locale.then(function () {
            _.each($(".input-group.date"), function (date_field) {
                let minDate =
                    $(date_field).data("mindate") || moment({y: 1900});
                let maxDate =
                    $(date_field).data("maxdate") || moment().add(200, "y");
                let options = {
                    minDate: minDate,
                    maxDate: maxDate,
                    calendarWeeks: true,
                    icons: {
                        time: "fa fa-clock-o",
                        date: "fa fa-calendar",
                        next: "fa fa-chevron-right",
                        previous: "fa fa-chevron-left",
                        up: "fa fa-chevron-up",
                        down: "fa fa-chevron-down",
                    },
                    locale: moment.locale(),
                    allowInputToggle: true,
                    keyBinds: null,
                };
                if ($(date_field).find(".o_website_form_date").length > 0) {
                    options.format = time.getLangDateFormat();
                } else if (
                    $(date_field).find(".o_website_form_clock").length > 0
                ) {
                    // options.format = time.getLangTimeFormat();
                    options.format = "HH:mm";
                    options.defaultDate = moment("00:00", "HH:mm");
                } else {
                    options.format = time.getLangDatetimeFormat();
                }
                $("#" + date_field.id).datetimepicker(options);
            });
        });
    }
);
