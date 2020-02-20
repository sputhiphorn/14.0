"use strict";
odoo.define('pos_extend.screens', function (require) {

    var models = require('point_of_sale.models');
    var screens = require('point_of_sale.screens');
    var core = require('web.core');
    var utils = require('web.utils');
    var round_pr = utils.round_precision;
    var _t = core._t;
    var gui = require('point_of_sale.gui');
    var qweb = core.qweb;

    var rpc = require('web.rpc');
    var currency_rate=1;

    screens.ReceiptScreenWidget.include({
        renderElement: function () {
            var self = this;
            this._super();
            this.$('.back_order').click(function () {
                var order = self.pos.get_order();
                if (order) {
                    self.pos.gui.show_screen('products');
                }
            });
        },
        show: function () {
            this._super();
            try {
                JsBarcode("#barcode", this.pos.get('selectedOrder').ean13, {
                    format: "EAN13",
                    displayValue: true,
                    fontSize: 20
                });
            } catch (error) {
            }
        }
    });

    screens.OrderWidget.include({
         renderElement: function () {
            var order = this.pos.get_order();
            rpc.query({
                    model: 'res.currency',
                    method: 'get_convert_rate',
                    args: ["KHR"]
            }).then(function (value) {
                if (value) {
                    currency_rate=value.rate;
                    if (order) {
                        order.exchange_rate = currency_rate;
                    }
                }
            });
            this._super();
         },
         change_selected_order: function () {
            var order = this.pos.get_order();
            if (order) {
                order.exchange_rate = currency_rate;
            }
            this._super();
         }
    });
    return screens;
});
