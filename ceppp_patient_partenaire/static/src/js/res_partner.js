odoo.define('ceppp_patient_partenaire.res_partner_open_chat', function (require) {
    var Widget = require('web.Widget');
    var widgetRegistry = require('web.widget_registry');
    var FieldManagerMixin = require('web.FieldManagerMixin');
    var rpc = require('web.rpc')
    var core = require('web.core');
    var Discuss = require('mail.Discuss');

    var WidgetResPartnerCepppDiscuss = Widget.extend(FieldManagerMixin, {
    init: function (parent, model, context) {
        this._super(parent);
        FieldManagerMixin.init.call(this);
        this._super.apply(this, arguments);
        this.activeId = model.model == "res.partner" && model.res_id || false;
        this.channel_id = 0;
        this.menu_id = 0;
        this.action_id = 0;
        this.is_new = false;
    },

    start: function() {
        var self = this;
        this._super.apply(this, arguments);
        var html ='<button id="btn_open_discuss" class="btn btn-secondary"><i class="fa fa-wechat"/> Clavardage</button>';
        this.$el.html(html);
        this.$('#btn_open_discuss').click(function(ev){
            if (self.activeId === false) {
                return;
            }
            //            rpc.query({
            //                model: 'mail.channel',
            //                method: 'channel_get',
            //                args: [[self.activeId]],
            //            })
            rpc.query({
                model: 'res.partner',
                method: 'open_partner_discuss',
                args: [[self.activeId]],
            })
            .then(function (result) {
                if (typeof result!=='object') {
                    return;
                }
                self.channel_id = result.channel_id;
                self.menu_id = result.menu_id;
                self.action_id = result.action_id;
                self.is_new = result.is_new;
                self.do_action('mail.action_discuss', { active_id: self.channel_id })
                .then(function () {
                    // we cannot 'go back to previous page' otherwise
                    self.trigger_up('hide_home_menu');
                    core.bus.trigger('change_menu_section', self.call('mail_service', 'getDiscussMenuID'));
                    console.debug("Redirect action_discuss id channel " + self.channel_id);
                    const urlParams = new URLSearchParams(window.location.href);
                    const mailbox_inbox = urlParams.get('active_id')
                    if (mailbox_inbox == "mailbox_inbox") {
                        console.debug("New channel res_partner, force reload it, bug!");
                        var new_url = "/web#action=" + self.action_id + "&menu_id=" + self.menu_id + "&active_id=" + self.channel_id;
                        console.debug(new_url);
                        window.location.replace(new_url);
                        location.reload(true);
                    }
                });
            });
        });
    },
});

widgetRegistry.add(
    'widget_redirect_from_res_partner_to_discuss', WidgetResPartnerCepppDiscuss
);

});
