odoo.define('bill_separate_categories.model', function (require) {
"use strict";

    var models = require('point_of_sale.models');  
    var core = require('web.core');

    var _t = core._t;
   
    var _super_Order = models.Order.prototype;
    models.Order = models.Order.extend({
        computeChanges: function(categories) {
            var current_res = this.build_line_resume();
            var old_res     = this.saved_resume || {};
            var json        = this.export_as_JSON();
            var add = [];
            var rem = [];
            var line_hash;

            for ( line_hash in current_res) {
                var curr = current_res[line_hash];
                var old  = old_res[line_hash];

                if (typeof old === 'undefined') {
                    add.push({
                        'id':       curr.product_id,
                        'name':     this.pos.db.get_product_by_id(curr.product_id).display_name,
                        'name_wrapped': curr.product_name_wrapped,
                        'note':     curr.note,
                        'qty':      curr.qty,
                        'categ':   this.pos.db.get_product_by_id(curr.product_id).pos_categ_id,
                    });
                } else if (old.qty < curr.qty) {
                    add.push({
                        'id':       curr.product_id,
                        'name':     this.pos.db.get_product_by_id(curr.product_id).display_name,
                        'name_wrapped': curr.product_name_wrapped,
                        'note':     curr.note,
                        'qty':      curr.qty - old.qty,
                        'categ':   this.pos.db.get_product_by_id(curr.product_id).pos_categ_id,
                    });
                } else if (old.qty > curr.qty) {
                    rem.push({
                        'id':       curr.product_id,
                        'name':     this.pos.db.get_product_by_id(curr.product_id).display_name,
                        'name_wrapped': curr.product_name_wrapped,
                        'note':     curr.note,
                        'qty':      old.qty - curr.qty,
                        'categ':   this.pos.db.get_product_by_id(curr.product_id).pos_categ_id,
                    });
                }
            }

            for (line_hash in old_res) {
                if (typeof current_res[line_hash] === 'undefined') {
                    var old = old_res[line_hash];
                    rem.push({
                        'id':       old.product_id,
                        'name':     this.pos.db.get_product_by_id(old.product_id).display_name,
                        'name_wrapped': old.product_name_wrapped,
                        'note':     old.note,
                        'qty':      old.qty, 
                        'categ':   this.pos.db.get_product_by_id(old.product_id).pos_categ_id,
                    });
                }
            }

            if (categories && categories.length > 0) {
                // filter the added and removed orders to only contains
                // products that belong to one of the categories supplied as a parameter

                var self = this;

                var _add = [];
                var _rem = [];
                
                for (var i = 0; i < add.length; i++) {
                    if (self.pos.db.is_product_in_category(categories,add[i].id)) {
                        _add.push(add[i]);
                    }
                }
                add = _add;

                for (var i = 0; i < rem.length; i++) {
                    if (self.pos.db.is_product_in_category(categories,rem[i].id)) {
                        _rem.push(rem[i]);
                    }
                }
                rem = _rem;
            }

            var d = new Date();
            var hours   = '' + d.getHours();
                hours   = hours.length < 2 ? ('0' + hours) : hours;
            var minutes = '' + d.getMinutes();
                minutes = minutes.length < 2 ? ('0' + minutes) : minutes;
            var today = new Date();
            var currentday = today.getDate();
            var currentmonth = today.getMonth() + 1; //January is 0!
            var currentyear = today.getFullYear();

            if (currentday < 10) {
                currentday = '0' + currentday;
            }

            if (currentmonth < 10) {
                currentmonth = '0' + currentmonth;
            }

            today = currentday + '/' + currentmonth + '/' + currentyear;

            return {
                'new': add,
                'cancelled': rem,
                'table': json.table || false,
                'floor': json.floor || false,
                'name': json.name  || 'unknown order',
                'time': {
                    'hours': hours,
                    'minutes': minutes,
                    'today': today,
                },
                'list_product_category_new': this.get_list_product_category(add),
                'list_product_category_cancelled': this.get_list_product_category(rem),
                'list_pos_category': this.pos.db.category_by_id,
                'labeltext': {
                    'CANCELLED': _t('CANCELLED'),
                    'NEW': _t('NEW'),
                    'Floor': _t('Floor:'),
                    'Table': _t('Table:'),
                    'Qty': _t('Qty='),
                    'End': _t('.............................END..........................'),
                },
                'separate_category': this.pos.config.separate_category
            };
        },

        get_list_product_category: function(list_product) {
            var list_product_category = [];
            var list_cat_id = [];
            for (var i = 0; i < list_product.length; i++) {
                if(list_product_category.length === 0) {
                    list_product_category.push(list_product[i].categ);
                    list_cat_id.push(list_product[i].categ[0]);
                } else {
                    if (!(list_cat_id.includes(list_product[i].categ[0]))) {
                        list_product_category.push(list_product[i].categ);
                        list_cat_id.push(list_product[i].categ[0]);
                    } 
                }
            }
            return list_product_category;
        }, 
    })

    var _super_Orderline = models.Orderline.prototype;
    models.Orderline = models.Orderline.extend({
        export_for_printing: function() {
            var data = _super_Orderline.export_for_printing.apply(this, arguments);
            data.category = this.get_product().categ;
            return data;
        },
    })
});