odoo.define('pos_global_discount.base', function (require) {
"use strict";

    var Widget = require('web.Widget');

    var PosWidget = Widget.include({
        format_percentage: function(amount){
            var symbol = '%'
            return amount + ' ' + symbol;
        },
    });
    return PosWidget;
});
