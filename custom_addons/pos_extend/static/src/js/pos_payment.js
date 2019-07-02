odoo.define('pos_extend.other_currency_payment', function (require) {
"use strict";

var screens = require('point_of_sale.screens');
var PaymentScreenWidget = screens.PaymentScreenWidget;
var core = require('web.core');
var gui = require('point_of_sale.gui');


var _t = core._t;


PaymentScreenWidget.include({
    renderElement: function() {
        var self = this;
        this._super();
        this.$('.js_pay_in_other_currency').click(function(){
            self.click_payment_in_other_currency();
        });
    },
    click_payment_in_other_currency: function(){
        var self = this;
        var convert_rate=1;
        if(self.pos.get_order().exchange_rate){
            convert_rate=self.pos.get_order().exchange_rate
        }
        var amount_due=self.pos.get_order().get_due();
        var amount_in_other_currency=this.format_currency_no_symbol(amount_due* convert_rate);
        if(amount_due>0){
            this.gui.show_popup('payment_pad',{
                                'title':  'Payment In Riel ( 1$='+self.format_currency_no_symbol(convert_rate)+'៛)',
                                'amount':"៛ "+amount_in_other_currency,
                                'after_certain':function(){
                                    var input_amount=this.inputbuffer/convert_rate;
                                    self.set_payment(input_amount.toFixed(3));
                                },
                            });
        }
    },
    set_payment: function(value){
        var self = this;
        var paymentlines = this.pos.get_order().get_paymentlines();
	    var open_paymentline = false;
	    var payment_line = null;
        var cashregister = null;
        var order =this.pos.get_order();
        if (! open_paymentline){
            cashregister = self.pos.cashregisters[0];
            this.pos.get_order().add_paymentline(cashregister);
            this.reset_input();
            this.render_paymentlines();
            this.payment_input(value);
        }
        else{

            this.pos.get_order().select_paymentline(payment_line);
            this.reset_input();
            this.render_paymentlines();
            this.payment_input(payment_line.amount+value);
        }
    }
});


});