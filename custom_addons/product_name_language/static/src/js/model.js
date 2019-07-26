odoo.define('product_name_language.model', function (require) {
    var models = require('point_of_sale.models');   
    var rpc = require('web.rpc');     


    models.load_fields("product.product",['other_language_name']);

    var _super_orderline = models.Orderline.prototype;

    models.Orderline = models.Orderline.extend({
        initialize: function(attr,options){
            _super_orderline.initialize.apply(this,arguments);            
        },

        export_as_JSON: function() {
            var data = _super_orderline.export_as_JSON.apply(this, arguments);
            data.other_language_name = this.other_language_name;
            return data;
        },

        init_from_JSON: function(json) {
            this.other_language_name = json.other_language_name;
            _super_orderline.init_from_JSON.call(this, json);
        },
    });
   
});