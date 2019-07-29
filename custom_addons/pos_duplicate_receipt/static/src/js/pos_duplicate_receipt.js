// This module open source
// Design and development by: TL Technology (thanhchatvn@gmail.com)
odoo.define('pos_duplicate_receipt', function (require) {
    var screens = require('point_of_sale.screens');
    var core = require('web.core');
    var qweb = core.qweb;

    screens.ReceiptScreenWidget.include({
        render_receipt: function () {
            this._super();
            if (this.pos.config.duplicate_receipt && this.pos.config.print_number > 1) {
                var contents = $('.pos-receipt-container');
                var i = 1;
                while (i < this.pos.config.print_number) {
                    contents.append(qweb.render('PosTicket', this.get_receipt_render_env()));
                    i++;
                }
            }
        },
        print_xml: function () {
            if (this.pos.config.duplicate_receipt && this.pos.config.print_number > 1) {
                var i = 1;
                while (i <= this.pos.config.print_number) {
                    var receipt = qweb.render('XmlReceipt', this.get_receipt_render_env());
                    this.pos.proxy.print_receipt(receipt);
                    i++;
                }
                this.pos.get_order()._printed = true;
            } else {
                return this._super();
            }
        }
    })
});
