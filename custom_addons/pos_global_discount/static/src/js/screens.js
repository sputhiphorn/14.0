odoo.define('pos_global_discount.screens', function (require) {
"use strict";

    var models = require('point_of_sale.models');
    var screens = require('pos_extend.screens');
    var core = require('web.core');
    var utils = require('web.utils');
    var round_pr = utils.round_precision;
    var _t = core._t;
    var gui = require('point_of_sale.gui');
    var qweb = core.qweb;

    var rpc = require('web.rpc');

    screens.OrderWidget.include({
        set_value: function(val) {
            var order = this.pos.get_order();
            if (order.get_selected_orderline()) {
                var mode = this.numpad_state.get('mode');
                if( mode === 'quantity'){
                    order.get_selected_orderline().set_quantity(val);
                }else if( mode === 'discount'){
                    if(order.get_global_discount_percentage() === 0){
                        order.get_selected_orderline().set_discount(val);
                    } else{
                        this.gui.show_popup('error',{
                            'title': _t('Global discount already set.'),
                            'body': _t('You can\'t set a local discount when the global discount is different to 0'),
                        });
                    }
                }else if( mode === 'price'){
                    var selected_orderline = order.get_selected_orderline();
                    selected_orderline.price_manually_set = true;
                    selected_orderline.set_unit_price(val);
                }
            }
        },

        update_summary: function(){
            this._super();
            var order = this.pos.get_order();
            var global_discount  = order ? order.get_global_discount_percentage() : 0;
            var global_discount_value = order ? order.get_global_discount_value() : 0;
            var taxes = order ? order.get_total_tax() : 0; 
            if(order.get_total_with_tax() !== 0){
                this.el.querySelector('.summary div.subentry_discount > span.discount').textContent = this.format_percentage(global_discount);
                this.el.querySelector('.summary div.subentry_discount > span.disc_value').textContent = this.format_currency(global_discount_value)
                this.el.querySelector('.summary .total .subentry .value').textContent = this.format_currency(taxes);
            }
        },
    });
});
