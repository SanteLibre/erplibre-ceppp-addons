odoo.define(
    "ceppp_patient_partenaire.ceppp_patient_partenaire_portal",
    function (require) {
        "use strict";

        require("web.dom_ready");
        let time = require("web.time");
        let rpc = require('web.rpc');
        let ajax = require("web.ajax");
        let base = require("web_editor.base");
        let core = require('web.core');
        let _t = core._t;
        let context = require("web_editor.context");

        // Autocomplete
        const element = document.getElementById("maladie");
        if (element) {
            const autoCompleteJS = new autoComplete({
                selector: "#maladie",
                data: {
                    cache: true,
                    src: async (query) => {
                      try {
                        // Fetch Data from external Source
                        const source = await rpc.query({
                            route: "/ceppp_maladie_list_autocomplete",
                            params: {
                                query: query,
                            },
                        });
                        // Data should be an array of `Objects` or `Strings`
                        const data = await source;
                        console.debug(data);
                        return data;
                      } catch (error) {
                        console.error(error);
                        return error;
                      }
                    },
                },
                query: (query) => {
                    // Split query into array
                    const querySplit = query.split(";");
                    // Get last query value index
                    const lastQuery = querySplit.length - 1;
                    // Trim new query
                    const newQuery = querySplit[lastQuery].trim();

                    return newQuery;
                },
                events: {
                    input: {
                        selection(event) {
                            const feedback = event.detail;
                            const input = autoCompleteJS.input;
                            // Trim selected Value
                            const selection = feedback.selection.value.trim();
                            // Split query into array and trim each value
                            const query = input.value.split(";").map(item => item.trim());
                            // Remove last query
                            query.pop();
                            // Add selected value
                            query.push(selection);
                            // Replace Input value with the new query
                            input.value = query.join("; ") + "; ";
                        },
                        focus() {
                            const inputValue = autoCompleteJS.input.value;
                            if (inputValue.length) autoCompleteJS.start();
                        },
//                        open() {
//                            // Dynamic position
//                            const position =
//                                autoCompleteJS.input.getBoundingClientRect().bottom + autoCompleteJS.list.getBoundingClientRect().height >
//                                (window.innerHeight || document.documentElement.clientHeight);
//
//                            if (position) {
//                                autoCompleteJS.list.style.bottom = autoCompleteJS.input.offsetHeight + 8 + "px";
//                            } else {
//                                autoCompleteJS.list.style.bottom = -autoCompleteJS.list.offsetHeight - 8 + "px";
//                            }
//                        },
                    }
                },
                resultItem: {
                    tag: "li",
                    class: "autoComplete_result",
//                    element: (item, data) => {
//                        item.setAttribute("data-parent", "food-item");
//                    },
                    highlight: "autoComplete_highlight",
                    selected: "autoComplete_selected"
                },
//                searchEngine: "loose",
//                searchEngine: "strict",
            });
        }

        // delete button
        $("#trash_maladie").on("click", function (event) {
            event.preventDefault();
            let text = _t("Êtes-vous certains de vouloir effacer cette expérience, votre action sera irrévocable.");
            if (confirm(text) == true) {
                rpc.query({
                    model: 'ceppp.maladie_personne_affectee',
                    method: 'unlink',
                    args: [[parseInt($('.modifier_maladie_form .ceppp_maladie_id').val())]],
                })
                .fail(function () {
                    alert(_t("Une erreur est survenue au moment d'effacer cette donnée en lien avec cette expérience. Veuillez informer votre recruteur, merci."))
                })
                .done(function () {
                    window.location.href = "/my/ceppp_maladie_personne_affectees";
                });
            }
        });
        $("#trash_formation").on("click", function (event) {
            event.preventDefault();
            let text = _t("Êtes-vous certains de vouloir effacer cette formation, votre action sera irrévocable.");
            if (confirm(text) == true) {
                rpc.query({
                    model: 'ceppp.formation',
                    method: 'unlink',
                    args: [[parseInt($('.modifier_formation_form .ceppp_formation_id').val())]],
                })
                .fail(function () {
                    alert(_t("Une erreur est survenue au moment d'effacer cette donnée en lien avec cette formation. Veuillez informer votre recruteur, merci."))
                })
                .done(function () {
                    window.location.href = "/my/ceppp_formations";
                });
            }
        });
        $("#trash_implication").on("click", function (event) {
            event.preventDefault();
            let text = _t("Êtes-vous certains de vouloir effacer cette implication, votre action sera irrévocable.");
            if (confirm(text) == true) {
                rpc.query({
                    model: 'ceppp.implication',
                    method: 'unlink',
                    args: [[parseInt($('.modifier_implication_form .ceppp_implication_id').val())]],
                })
                .fail(function () {
                    alert(_t("Une erreur est survenue au moment d'effacer cette donnée en lien avec cette implication. Veuillez informer votre recruteur, merci."))
                })
                .done(function () {
                    window.location.href = "/my/ceppp_implications";
                });
            }
        });

        // Support autre rôle
        function check_role_autre () {
            let n = $("input[id^='role_Autre_']:checked").length;
            if (n > 0) {
                $('#div_autre_role').show();
            } else {
                $('#div_autre_role').hide();
            }
        }

        check_role_autre();

        $("input[id^='role_Autre_']").on("click", function (event) {
            // event.preventDefault();
            check_role_autre();
        });

        // Support autre langue
        function check_langue_autre () {
            let n = $("input[id^='langue_parle_ecrit_Autre_']:checked").length;
            if (n > 0) {
                $('#div_autre_langue').show();
            } else {
                $('#div_autre_langue').hide();
            }
        }

        check_langue_autre();

        $("input[id^='langue_parle_ecrit_Autre_']").on("click", function (event) {
            // event.preventDefault();
            check_langue_autre();
        });

        // Support autre occupation
        function check_occupation_autre () {
            let n = $("input[id^='occupation_Autre_']:checked").length;
            if (n > 0) {
                $('#div_autre_occupation').show();
            } else {
                $('#div_autre_occupation').hide();
            }
        }

        check_occupation_autre();

        $("input[id^='occupation_Autre_']").on("click", function (event) {
            // event.preventDefault();
            check_occupation_autre();
        });

        // Support autre domaine
        function check_domaine_autre () {
            let n = $("input[id^='domaine_Autre_']:checked").length;
            if (n > 0) {
                $('#div_autre_domaine').show();
            } else {
                $('#div_autre_domaine').hide();
            }
        }

        check_domaine_autre();

        $("input[id^='domaine_Autre_']").on("click", function (event) {
            // event.preventDefault();
            check_domaine_autre();
        });

        // Support autre relation
        function check_relation_autre () {
            let n = $("input[id^='relation_Autre_']:checked").length;
            if (n > 0) {
                $('#div_autre_relation').show();
            } else {
                $('#div_autre_relation').hide();
            }
        }

        check_relation_autre();

        $("input[id^='relation_Autre_']").on("click", function (event) {
            // event.preventDefault();
            check_relation_autre();
        });

        // Support autre formation
        function check_formation_autre () {
            let n = $("input[id^='titre_formation_Autre_']:checked").length;
            if (n > 0) {
                $('#div_autre_formation').show();
            } else {
                $('#div_autre_formation').hide();
            }
        }

        check_formation_autre();

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

        $('.modifier_formation_confirm').on('click', function () {
            var $btn = $(this);
            $btn.prop('disabled', true);

            var selectedTitreFormationIds = [];
            $('.modifier_formation_form .titre_formation:checked').each(function () {
                selectedTitreFormationIds.push(parseInt($(this).val()));
            });

            rpc.query({
                model: 'ceppp.formation',
                method: 'update_formation_portal',
                args: [[parseInt($('.modifier_formation_form .ceppp_formation_id').val())], {
                    organisation: $('.modifier_formation_form .organisation').val(),
                    date: $('.modifier_formation_form .date_formation').val(),
                    date_fin: $('.modifier_formation_form .date_fin_formation').val(),
                    titre_formation: selectedTitreFormationIds,
                    titre_formation_autre: $('.modifier_formation_form .titre_formation_autre').val(),
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

        $('.modifier_consentement_confirm').on('click', function () {
            var $btn = $(this);
            $btn.prop('disabled', true);

            rpc.query({
                model: 'ceppp.recruteur',
                method: 'update_recruteur_consentement_portal',
                args: [[parseInt($('.modifier_consentement_form .ceppp_recruteur_id').val())], {
                    consentement_notification: $('.modifier_consentement_form #check_consentement_notification').is(":checked"),
                    consentement_recrutement: $('.modifier_consentement_form #check_consentement_recrutement').is(":checked"),
                    consentement_recherche: $('.modifier_consentement_form #check_consentement_recherche').is(":checked"),
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

        $('.modifier_preference_confirm').on('click', function () {
            var $btn = $(this);
            $btn.prop('disabled', true);

            var selectedModeCommPriviIds = [];
            $('.modifier_preference_form .mode_communication_privilegie:checked').each(function () {
                // Ajout de l'ID de la checkbox au tableau
                selectedModeCommPriviIds.push(parseInt($(this).val()));
            });

            var selectedDispoIds = [];
            $('.modifier_preference_form .disponibilite:checked').each(function () {
                // Ajout de l'ID de la checkbox au tableau
                selectedDispoIds.push(parseInt($(this).val()));
            });

            var selectedNotDispoIds = [];
            $('.modifier_preference_form .disponibilite_not:checked').each(function () {
                // Ajout de l'ID de la checkbox au tableau
                selectedNotDispoIds.push(parseInt($(this).val()));
            });

            rpc.query({
                model: 'ceppp.recruteur',
                method: 'update_recruteur_preference_portal',
                args: [[parseInt($('.modifier_preference_form .ceppp_recruteur_id').val())], {
                    mode_communication_privilegie: selectedModeCommPriviIds,
                    disponibilite: selectedDispoIds,
                    disponibilite_not: selectedNotDispoIds,
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
                    maladie: $('.modifier_maladie_form .maladie').val(),
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
        check_langue_autre();
        check_occupation_autre();
        check_domaine_autre();
        check_relation_autre();
        check_formation_autre();
    });

    $('.modal_modifier_consentement').on('hide.bs.modal', function (e) {
        // Force reload information, the code will be more simple
        // bug occur, the data is not restored
        location.reload(true);
    });

    $('.modal_modifier_preference').on('hide.bs.modal', function (e) {
        // Force reload information, the code will be more simple
        // bug occur, the data is not restored
        location.reload(true);
    });

    $('.modal_modifier_formation').on('hide.bs.modal', function (e) {
        // Force reload information, the code will be more simple
        // bug occur, the data is not restored
        location.reload(true);
    });

    $('.modal_modifier_implication').on('hide.bs.modal', function (e) {
        // Force reload information, the code will be more simple
        // bug occur, the data is not restored
        location.reload(true);
    });

    $('.modal_modifier_maladie').on('hide.bs.modal', function (e) {
        // Force reload information, the code will be more simple
        // bug occur, the data is not restored
        location.reload(true);
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
