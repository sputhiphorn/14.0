odoo.define('pos_extend.paymentpad', function (require) {
    "use strict";
    var models = require('point_of_sale.models');
    var screens = require('point_of_sale.screens');
    var gui = require('point_of_sale.gui');
    var core = require('web.core');
    var QWeb = core.qweb;
    var rpc = require('web.rpc');

    for (var index in gui.Gui.prototype.popup_classes) {
        if(gui.Gui.prototype.popup_classes[index].name=='number'){
            var NumberWidget = gui.Gui.prototype.popup_classes[index].widget;
            var PaymentPadWidget = NumberWidget.extend({
                template: 'PaymentPadWidget',
                click_confirm: function(){
                    var self = this;
                    this.gui.close_popup();
                    self.options.after_certain.call(self);
                },
            });
            gui.define_popup({name:'payment_pad', widget: PaymentPadWidget});
            break;
        }
    }

});