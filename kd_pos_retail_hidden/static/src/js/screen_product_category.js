odoo.define('kd_pos_retail_hidden.screen_product_category', function (require) {
"use strict";
    // **************************************************************************
    // Hidden Button Home Depend on Set Start Category in Configuration
    // **************************************************************************

    var screens = require('point_of_sale.screens');
    var core = require('web.core');
    var QWeb = core.qweb;

    screens.ProductCategoriesWidget.include({
        renderElement: function(){

            var el_str  = QWeb.render(this.template, {widget: this});
            var el_node = document.createElement('div');

            el_node.innerHTML = el_str;
            el_node = el_node.childNodes[1];

            if(this.el && this.el.parentNode){
                this.el.parentNode.replaceChild(el_node,this.el);
            }

            this.el = el_node;

            var withpics = this.pos.config.iface_display_categ_images;

            var list_container = el_node.querySelector('.category-list');
            if (list_container) {
                if (!withpics) {
                    list_container.classList.add('simple');
                } else {
                    list_container.classList.remove('simple');
                }
                for(var i = 0, len = this.subcategories.length; i < len; i++){
                    list_container.appendChild(this.render_category(this.subcategories[i],withpics));
                }
            }

            var buttons = el_node.querySelectorAll('.js-category-switch');
            var buttons_home = el_node.querySelectorAll('.breadcrumb-home');
            if (this.pos.config.iface_start_categ_id) {
                buttons_home[0].parentNode.removeChild(buttons_home[0]);
            }
            for(var i = 0; i < buttons.length; i++){
                buttons[i].addEventListener('click',this.switch_category_handler);
            }

            var products = this.pos.db.get_product_by_category(this.category.id);
            this.product_list_widget.set_product_list(products); // FIXME: this should be moved elsewhere ...

            this.el.querySelector('.searchbox input').addEventListener('keypress',this.search_handler);

            this.el.querySelector('.searchbox input').addEventListener('keydown',this.search_handler);

            this.el.querySelector('.search-clear').addEventListener('click',this.clear_search_handler);

            if(this.pos.config.iface_vkeyboard && this.chrome.widget.keyboard){
                this.chrome.widget.keyboard.connect($(this.el.querySelector('.searchbox input')));
            }
        },
    })
});