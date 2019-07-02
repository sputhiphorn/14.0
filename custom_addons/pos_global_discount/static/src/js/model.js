odoo.define('pos_global_discount.model', function (require) {
"use strict";
    
    var models = require('point_of_sale.models');    
    var utils = require('web.utils');
    var core = require('web.core');

    var _t = core._t;
    var round_pr = utils.round_precision;

    var _super_Order = models.Order.prototype;

    models.Orderline = models.Orderline.extend({
        get_all_prices: function() {
            if (this.order.global_discount === 0) {
                var price_unit = this.get_unit_price() * (1.0 - (this.get_discount() / 100.0));
            } else {
                var price_unit = this.get_unit_price()
            }
            var taxtotal = 0;
    
            var product =  this.get_product();
            var taxes_ids = product.taxes_id;
            var taxes =  this.pos.taxes;
            var taxdetail = {};
            var product_taxes = [];
    
            _(taxes_ids).each(function(el) {
                product_taxes.push(_.detect(taxes, function(t) {
                    return t.id === el;
                }));
            });
    
            var all_taxes = this.compute_all(product_taxes, price_unit, this.get_quantity(), this.pos.currency.rounding);
            _(all_taxes.taxes).each(function(tax) {
                taxtotal += tax.amount;
                taxdetail[tax.id] = tax.amount;
            });
    
            return {
                "priceWithTax": all_taxes.total_included,
                "priceWithoutTax": all_taxes.total_excluded,
                "tax": taxtotal,
                "taxDetails": taxdetail,
            };
        },
        get_base_price: function() {
            var rounding = this.pos.currency.rounding;
            if (this.order.global_discount === 0) {
                return round_pr(this.get_unit_price() * this.get_quantity() * (1 - this.get_discount()/100), rounding);
            } else {
                return round_pr(this.get_unit_price() * this.get_quantity(), rounding);
            }
        }
    });

    models.Order = models.Order.extend({
        initialize: function(attributes,options) {
            this.global_discount = 0;
            _super_Order.initialize.apply(this, arguments);
        },
        
        init_from_JSON: function(json) {
            var res = _super_Order.init_from_JSON.apply(this, arguments);
            this.global_discount = json.global_discount; 

            return res;
        },
        export_as_JSON: function() {
            var data = _super_Order.export_as_JSON.apply(this, arguments);
            data.global_discount = this.global_discount;
            
            return data;
        },

        export_for_printing: function() {
            var receipt = _super_Order.export_for_printing.apply(this, arguments);
            
            receipt.global_discount_value =  this.get_global_discount_value();
            receipt.global_discount_percentage = this.get_global_discount_percentage();
            
            return receipt;
        },

        add_product: function(product, options) {
            if (this._printed) {
                this.destroy();
                return this.pos.get_order().add_product(product, options);
            }
            this.assert_editable();
            options = options || {};
            var attr = JSON.parse(JSON.stringify(product));
            attr.pos = this.pos;
            attr.order = this;
            var line = new models.Orderline({}, {pos: this.pos, order: this, product: product});

            if (options.quantity !== undefined) {
                line.set_quantity(options.quantity);
            }

            if (options.price !== undefined) {
                line.set_unit_price(options.price);
            }

            //To substract from the unit price the included taxes mapped by the fiscal position
            this.fix_tax_included_price(line);
        
            if (this.global_discount === 0) {
                if(options.discount !== undefined){
                    line.set_discount(options.discount);
                }
            } else {
                line.set_discount(this.global_discount);
            }

            if (options.extras !== undefined) {
                for (var prop in options.extras) {
                    line[prop] = options.extras[prop];
                }
            }

            var to_merge_orderline;
            for (var i = 0; i < this.orderlines.length; i++) {
                if (this.orderlines.at(i).can_be_merged_with(line) && options.merge !== false) {
                    to_merge_orderline = this.orderlines.at(i);
                }
            }
            if (to_merge_orderline) {
                to_merge_orderline.merge(line);
            } else {
                this.orderlines.add(line);
            }
            this.select_orderline(this.get_last_orderline());

            if (line.has_product_lot) {
                this.display_lot_popup();
            }
        },

    
        get_total_without_discount: function() {
            var total = round_pr(this.orderlines.reduce((function(sum, orderLine) {
                return sum + orderLine.get_price_without_tax();
            }), 0), this.pos.currency.rounding);

            if (this.global_discount === 0) {
                return total + this.get_total_discount() + this.get_total_tax();
            } else {
                return total + this.get_total_tax();
            }
        },
    
        get_global_discount_value: function() {
            var total = this.get_total_without_tax() + this.get_total_tax();
            return round_pr(this.get_global_discount_percentage() * total / 100, this.pos.currency.rounding);
        },
    
        get_global_discount_percentage: function() {
            return this.global_discount;
        },
    
        set_global_discount: function(disc) {
            this.global_discount = disc;
            
            this.orderlines.each(function(line) {
                line.set_discount(disc);    
            });
        },

        get_total_with_tax: function() {
            var total = this.get_total_without_tax() + this.get_total_tax();
            if (this.global_discount === 0) {
                return total;
            } else {
                // get total with tax and then apply discount
                return total - total * this.get_global_discount_percentage() / 100;
            }
        },
        get_label_text: function () {
            var label_text = {
                label_date: _t('កាលបរិច្ឆេទ/Date:'),
                label_bill: _t('លេខវិក្កយបត្រ/Bill:'),
                label_receipt: _t('លេខវិក្កយបត្រ/Receipt:'),
                label_table: _t('លេខតុ/Table:'),
                label_pax: _t('ភ្ញៀវ/Pax:'),
                label_customer: _t('អតិថិជន/Customer:'),
                label_customerphone: _t('ទូរស័ព្ទ/M:'),
                label_desckh: _t('បរិយាយ'),
                label_qtykh: _t('ចំនួន'),
                label_pricekh: _t('តម្លៃ'),
                label_totalkh: _t('សរុប'),
                label_desc: _t('ITEMS'),
                label_qty: _t('QTY'),
                label_price: _t('PRICE'),
                label_total: _t('AMOUNT'),
                lable_with: _t('With a'),
                label_discount: _t('% discount'),
                label_subtotal: _t('សរុប/Subtotal:'),
                label_totaldiscount: _t('Total w/o discount:'),
                label_globaldiscount: _t('Global discount:'),
                label_discountkh: _t('បញ្ជុះតម្លៃ/Discount:'),
                label_totalusd: _t('Total(USD):'),
                label_grandtotalkh: _t('សរុបរួម(KHR):'),
                label_moneychange: _t('លុយអាប់/Change:'),
                label_thq: _t('Thank you for visiting and supporting'),
                label_shopname: _t('EHT Paul Dubrule'),
                label_t: _t('T:'),
                label_terminal: _t('Terminal:'),
                label_servedby: _t('Served By:')
            };
            return label_text;
        }
    });
});