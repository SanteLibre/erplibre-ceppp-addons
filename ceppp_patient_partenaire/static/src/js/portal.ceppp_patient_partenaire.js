odoo.define(
    "ceppp_patient_partenaire.ceppp_patient_partenaire_portal",
    function (require) {
        "use strict";

        require("web.dom_ready");
        let time = require("web.time");
        let rpc = require('web.rpc');
        let ajax = require("web.ajax");
        let base = require("web_editor.base");
        let context = require("web_editor.context");

        // Support autre rôle
        $('#div_autre_role').hide();

        function check_role_autre () {
            let n = $("input[id^='role_Autre_']:checked").length;
            if (n > 0) {
                $('#div_autre_role').show();
            } else {
                $('#div_autre_role').hide();
            }
        }

        $("input[id^='role_Autre_']").on("click", function (event) {
            // event.preventDefault();
            check_role_autre();
        });

        // Support autre domaine
        $('#div_autre_domaine').hide();

        function check_domaine_autre () {
            let n = $("input[id^='domaine_Autre_']:checked").length;
            if (n > 0) {
                $('#div_autre_domaine').show();
            } else {
                $('#div_autre_domaine').hide();
            }
        }

        $("input[id^='domaine_Autre_']").on("click", function (event) {
            // event.preventDefault();
            check_domaine_autre();
        });

        // Support autre relation
        $('#div_autre_relation').hide();

        function check_relation_autre () {
            let n = $("input[id^='relation_Autre_']:checked").length;
            if (n > 0) {
                $('#div_autre_relation').show();
            } else {
                $('#div_autre_relation').hide();
            }
        }

        $("input[id^='relation_Autre_']").on("click", function (event) {
            // event.preventDefault();
            check_relation_autre();
        });

        // Support autre formation
        $('#div_autre_formation').hide();

        function check_formation_autre () {
            let n = $("input[id^='titre_formation_Autre_']:checked").length;
            if (n > 0) {
                $('#div_autre_formation').show();
            } else {
                $('#div_autre_formation').hide();
            }
        }

        $("input[id^='titre_formation_Autre_']").on("click", function (event) {
            // event.preventDefault();
            check_formation_autre();
        });

        $('.modifier_implication_confirm').on('click', function () {
            var $btn = $(this);
            $btn.prop('disabled', true);

            var selectedDomaineIds = [];
            $('.modifier_implication_form .domaine:checked').each(function () {
                // Ajout de l'ID de la checkbox au tableau
                selectedDomaineIds.push(parseInt($(this).val()));
            });

            var selectedRoleIds = [];
            $('.modifier_implication_form .role:checked').each(function () {
                // Ajout de l'ID de la checkbox au tableau
                selectedRoleIds.push(parseInt($(this).val()));
            });

            rpc.query({
                model: 'ceppp.implication',
                method: 'update_implication_portal',
                args: [[parseInt($('.modifier_implication_form .ceppp_implication_id').val())], {
                    titre: $('.modifier_implication_form .titre').val(),
                    nom_equipe: $('.modifier_implication_form .nom_equipe').val(),
                    description: $('.modifier_implication_form .description').val(),
                    echeance_debut: $('.modifier_implication_form .echeance_debut').val(),
                    echeance_fin: $('.modifier_implication_form .echeance_fin').val(),
                    domaine: selectedDomaineIds,
                    domaine_autre: $('.modifier_implication_form .domaine_autre').val(),
                    role: selectedRoleIds,
                    role_autre: $('.modifier_implication_form .role_autre').val(),
                }],
            })
                .fail(function () {
                    $btn.prop('disabled', false);
                })
                .done(function () {
                    window.location.reload();
                });
            return false;
        });

        $('.modifier_maladie_confirm').on('click', function () {
            var $btn = $(this);
            $btn.prop('disabled', true);

            var selectedRelationIds = [];
            $('.modifier_maladie_form .relation:checked').each(function () {
                // Ajout de l'ID de la checkbox au tableau
                selectedRelationIds.push(parseInt($(this).val()));
            });

            rpc.query({
                model: 'ceppp.maladie_personne_affectee',
                method: 'update_maladie_portal',
                args: [[parseInt($('.modifier_maladie_form .ceppp_maladie_id').val())], {
                    detail_maladie: $('.modifier_maladie_form .detail_maladie').val(),
                    relation: selectedRelationIds,
                    relation_autre: $('.modifier_maladie_form .relation_autre').val(),
                }],
            })
                .fail(function () {
                    $btn.prop('disabled', false);
                })
                .done(function () {
                    window.location.reload();
                });
            return false;
        });

    function load_locale() {
        let url = "/web/webclient/locale/" + context.get().lang || "en_US";
        return ajax.loadJS(url);
    }

    $('body').on('shown.bs.modal', function (e) {
        datetimepicker_load();
        check_role_autre();
        check_domaine_autre();
        check_relation_autre();
        check_formation_autre();
    });

    function datetimepicker_load() {
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
//                    options.format = time.getLangDateFormat();
                    options.format = "YYYY-MM-DD";
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
        }

        let ready_with_locale = $.when(base.ready(), load_locale());
        ready_with_locale.then(datetimepicker_load());
    }
);
