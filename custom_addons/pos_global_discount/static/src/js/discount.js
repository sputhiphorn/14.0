odoo.define('pos_global_discount.discount', function (require) {
    "use strict";

    var core = require('web.core');
    var screens = require('point_of_sale.screens');
    
    var _t = core._t;
    
    var DiscountButton = screens.ActionButtonWidget.extend({
        template: 'GlobalDiscountButton',
        button_click: function(){
            var order = this.pos.get_order();
            this.gui.show_popup('number',{
                'title': _t('Discount Percentage'),
                'value': 0,
                'confirm': function(val) {
                    val = Math.round(Math.max(0,Math.min(100,val)));
                    order.set_global_discount(val);
                },
            });
        },
    });
    
    screens.define_action_button({
        'name': 'discount',
        'widget': DiscountButton,
    });
});
