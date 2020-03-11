"use strict";
odoo.define('pos_extend.order', function (require) {

    var utils = require('web.utils');
    var round_pr = utils.round_precision;
    var models = require('point_of_sale.models');
    var core = require('web.core');
    var qweb = core.qweb;
    var _t = core._t;

    var _super_Order = models.Order.prototype;
    models.Order = models.Order.extend({
        initialize: function (attributes, options) {
            _super_Order.initialize.apply(this, arguments);
        },
        init_from_JSON: function (json) {
            var res = _super_Order.init_from_JSON.apply(this, arguments);
            if (json.ean13) {
                this.ean13 = json.ean13;
            }
            this.exchange_rate=json.exchange_rate;
            return res;
        },
        export_as_JSON: function () {
            var json = _super_Order.export_as_JSON.apply(this, arguments);
            if (this.ean13) {
                json.ean13 = this.ean13;
            }
            if (!this.ean13 && this.uid) { // init ean13 and automatic create ean13 for order
                var ean13 = '998';
                if (this.pos.user.id) {
                    ean13 += this.pos.user.id;
                }
                if (this.sequence_number) {
                    ean13 += this.sequence_number;
                }
                if (this.pos.config.id) {
                    ean13 += this.pos.config.id;
                }
                var fean13 = this.uid.split('-');
                for (var i in fean13) {
                    ean13 += fean13[i];
                }
                ean13 = ean13.split('');
                var aean13 = [];
                var sean13 = '';
                for (var i = 0; i < ean13.length; i++) {
                    if (i < 12) {
                        sean13 += ean13[i];
                        aean13.push(ean13[i]);
                    }
                }
                this.ean13 = sean13 + this.generate_ean13(aean13).toString();
            }
            json.exchange_rate=this.exchange_rate;
            return json;
        },
        select_paymentline: function(line){
            if(line !== this.selected_paymentline){
                if(this.selected_paymentline){
                    this.selected_paymentline.set_selected(false);
                }
                this.selected_paymentline = line;
                if(this.selected_paymentline){
                    if (this.selected_paymentline.cashregister.journal_id[1].toLowerCase().indexOf("reil") >= 0) {
                        $('.select-currency').val('67');
                    }
                    else {
                        $('.select-currency').val('3');
                    }
                    $(".select-currency").trigger("change");
                    this.selected_paymentline.set_selected(true);
                }
                this.trigger('change:selected_paymentline',this.selected_paymentline);
            }
        },
        export_for_printing: function() {
	        var json = _super_Order.export_for_printing.apply(this,arguments);
	        if (this.ean13) {
                json.ean13 = this.ean13;
            }
            if (!this.ean13 && this.uid) { // init ean13 and automatic create ean13 for order
                var ean13 = '998';
                if (this.pos.user.id) {
                    ean13 += this.pos.user.id;
                }
                if (this.sequence_number) {
                    ean13 += this.sequence_number;
                }
                if (this.pos.config.id) {
                    ean13 += this.pos.config.id;
                }
                var fean13 = this.uid.split('-');
                for (var i in fean13) {
                    ean13 += fean13[i];
                }
                ean13 = ean13.split('');
                var aean13 = [];
                var sean13 = '';
                for (var i = 0; i < ean13.length; i++) {
                    if (i < 12) {
                        sean13 += ean13[i];
                        aean13.push(ean13[i]);
                    }
                }
                this.ean13 = sean13 + this.generate_ean13(aean13).toString();
            }
            json.exchange_rate=this.exchange_rate;
            return json;
	    },
        generate_ean13: function (code) {
            if (code.length != 12) {
                return -1;
            }
            var evensum = 0;
            var oddsum = 0;
            for (var i = 0; i < code.length; i++) {
                if ((i % 2) == 0) {
                    evensum += parseInt(code[i]);
                } else {
                    oddsum += parseInt(code[i]);
                }
            }
            var total = oddsum * 3 + evensum;
            return parseInt((10 - total % 10) % 10);
        },
        fix_tax_included_price: function (line) {
            _super_Order.fix_tax_included_price.apply(this, arguments);
            if (this.fiscal_position) {
                var unit_price = line.product['list_price'];
                var taxes = line.get_taxes();
                var mapped_included_taxes = [];
                _(taxes).each(function (tax) {
                    var line_tax = line._map_tax_fiscal_position(tax);
                    if (tax.price_include && tax.id != line_tax.id) {
                        mapped_included_taxes.push(tax);
                    }
                })
                if (mapped_included_taxes.length > 0) {
                    unit_price = line.compute_all(mapped_included_taxes, unit_price, 1, this.pos.currency.rounding, true).total_excluded;
                    line.set_unit_price(unit_price);
                }
            }
        },
        get_total_before_tax: function() {
		    return this.get_total_without_tax() + this.get_order_discount();
		},
		get_order_discount: function() {
			return round_pr(this.orderlines.reduce((function(sum, orderLine) {
				if (orderLine.get_product().display_name == 'Discount Product')
					return sum + Math.abs(orderLine.get_price_without_tax());
				else
				    return sum;
			}), 0), this.pos.currency.rounding);
		},
		get_total_in_other_currency: function() {
		    return  this.get_total_with_tax() / this.exchange_rate;
		},
        get_label_text: function () {
            var label_text = {
                label_t: _t('T:'),
                label_terminal: _t('Terminal:'),
                label_servedby: _t('Served By:'),
                label_date: _t('កាលបរិច្ឆេទ/Date:'),
                label_bill: _t("លេខវិក្កយបត្រ/Bill:"),
                label_receipt: _t('លេខវិក្កយបត្រ/Receipt:'),
                label_customer: _t('អតិថិជន/Customer:'),
                label_customerphone: _t('ទូរស័ព្ទ/M:'),
                label_desc: _t('បរិយាយ'),
                label_qtykh: _t('ចំនួន'),
                label_pricekh: _t('តម្លៃ'),
                label_total: _t('សរុប'),
                label_items: _t('ITEMS'),
                label_qty: _t('QTY'),
                label_price: _t('PRICE'),
                label_amount: _t('AMOUNT'),
                label_witha: _t('With a'),
                label_discount: _t('% discount'),
                label_subtotal: _t('សរុប/Subtotal:'),
                label_totalkh: _t('សរុបរួម(USD):'),
                label_totalus: _t('សរុប(KHR):'),
                label_moneychange: _t('លុយអាប់/Change:'),
                label_note: _t('Note:'),
                label_onedollar: _t('1$:'),
                label_thx: _t('Thank you for visiting and supporting')
            };
            return label_text;
        },
//        Multi Currency
        get_change: function (paymentline) {
            var change = _super_Order.get_change.apply(this, arguments);
            var client = this.get_client();
            var wallet_register = _.find(this.pos.cashregisters, function (register_journal) {
                return register_journal.journal['pos_method_type'] == 'wallet';
            }); // display wallet method when have change
            if (wallet_register) {
                var $journal_element = $("[data-id='" + wallet_register.journal['id'] + "']");
                if (change > 0 || (client && client['wallet'] > 0)) {
                    $journal_element.removeClass('oe_hidden');
                    $journal_element.addClass('highlight');
                } else {
                    $journal_element.addClass('oe_hidden');
                }
            }
            var company_currency = this.pos.company.currency_id; // return amount with difference currency
            if (paymentline && paymentline.cashregister && paymentline.cashregister.currency_id && paymentline.cashregister.currency_id[0] != company_currency[0]) {
                var new_change = -this.get_total_with_tax();
                var lines = this.paymentlines.models;
                var company_currency = this.pos.company.currency_id;
                var company_currency_data = this.pos.currency_by_id[company_currency[0]];
                for (var i = 0; i < lines.length; i++) {
                    var selected_currency = this.pos.currency_by_id[lines[i].cashregister.currency_id[0]];
                    var selected_rate = selected_currency['rate'];
                    var amount_of_line = lines[i].get_amount();
                    new_change += amount_of_line * selected_rate / company_currency_data['rate'];
                    if (lines[i] === paymentline) {
                        break;
                    }
                }
                var currency_change = round_pr(Math.max(0, new_change), this.pos.currency.rounding);
                if (currency_change > 0) {
                    this.active_button_add_wallet(true);
                } else {
                    this.active_button_add_wallet(false);
                }
                return currency_change
            }
            if (change > 0) {
                this.active_button_add_wallet(true);
            } else {
                this.active_button_add_wallet(false);
            }
            return change;
        },
        get_due: function (paymentline) {
            var due = _super_Order.get_due.apply(this, arguments);
            if (!paymentline) {
                return due;
            }
            var active_multi_currency = false;
            var lines = this.paymentlines.models;
            var company_currency = this.pos.company.currency_id;
            var company_currency_data = this.pos.currency_by_id[company_currency[0]];
            for (var i = 0; i < lines.length; i++) {
                var line = lines[i];
                var currency_id_of_line = line.cashregister.currency_id[0];
                var currency_of_line = this.pos.currency_by_id[currency_id_of_line];
                if (currency_of_line['id'] != company_currency_data['id']) {
                    active_multi_currency = true;
                }
            }
            var paymentline_currency_id = paymentline.cashregister.currency_id[0]
            var paymentline_currency = this.pos.currency_by_id[paymentline_currency_id];
            var payment_rate = paymentline_currency['rate'];
            if (paymentline_currency['id'] != company_currency_data['id']) {
                active_multi_currency = true
            }
            if (!active_multi_currency || active_multi_currency == false) {
                return due;
            } else {
                var total_amount_with_tax = this.get_total_with_tax();
                if (!payment_rate || payment_rate == 0) {
                    return due
                }
                var new_due = total_amount_with_tax * payment_rate / company_currency_data['rate'];
                var lines = this.paymentlines.models;
                for (var i = 0; i < lines.length; i++) {
                    if (lines[i] === paymentline) {
                        break;
                    } else {
                        var line = lines[i];
                        var line_cashregister = line['cashregister'];
                        var line_currency_rate = this.pos.currency_by_id[line_cashregister['currency_id'][0]]['rate'];
                        var line_amount = lines[i].get_amount() * line_currency_rate;
                        new_due -= line_amount * payment_rate / company_currency_data['rate'];
                    }
                }
                var new_due = round_pr(Math.max(0, new_due), this.pos.currency.rounding);
                return new_due
            }
        },
        get_total_paid: function () {
            var total_paid = _super_Order.get_total_paid.apply(this, arguments);
            var lines = this.paymentlines.models;
            var active_multi_currency = false;
            var total_paid_multi_currency = 0;
            for (var i = 0; i < lines.length; i++) {
                var line = lines[i];
                var currency = line.cashregister.currency_id;
                var company_currency = this.pos.company.currency_id;
                var company_currency_data = this.pos.currency_by_id[company_currency[0]];
                if (currency[0] != company_currency[0]) {
                    var register_currency = this.pos.currency_by_id[currency[0]];
                    var register_rate = register_currency['rate'];
                    active_multi_currency = true;
                    total_paid_multi_currency += line.get_amount() * register_rate / company_currency_data['rate'];
                } else {
                    total_paid_multi_currency += line.get_amount()
                }
            }
            if (active_multi_currency == true) {
                return round_pr(Math.max(0, total_paid_multi_currency), this.pos.currency.rounding);
            } else {
                return total_paid;
            }
        }
    });
    var _super_Orderline = models.Orderline.prototype;
    models.Orderline = models.Orderline.extend({
        get_item_discout: function() {
        	var discount = this.get_unit_price() * (this.get_discount() / 100.0);
        	return discount;        	
        },
        get_price_discount: function () { 
            var price_unit = this.get_unit_price();
            var prices = this.get_all_prices();
            var priceWithTax = prices['priceWithTax'];
            var tax = prices['tax'];
            var discount = priceWithTax - tax - price_unit;
            return discount;
        }
    });
});