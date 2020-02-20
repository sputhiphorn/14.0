/*
    This module create by: thanhchatvn@gmail.com
    License: OPL-1
    Please do not modification if i not accept
    Thanks for understand
 */
odoo.define('pos_extend.database', function (require) {
    var db = require('point_of_sale.DB');
    db.include({
        get_pos_orders: function (max_count) {
            var orders = [];
            var max = 0;
            for (var order_id in this.order_by_id) {
                this.order_by_id[order_id].name = this.order_by_id[order_id].pos_reference;
                orders.push(this.order_by_id[order_id]);
                max += 1;
                if (max_count > 0 && max >= max_count) {
                    break;
                }
            }
            return orders;
        },
    });
});
