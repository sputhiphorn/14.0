odoo.define('odoo_admin_tool.UserMenu', function (require) {
    "use strict";

    var UserMenu = require('web.UserMenu');
    UserMenu.include({
        init: function () {
            this._super.apply(this, arguments);
            var self = this;
            var session = this.getSession();

            self._rpc({
                model: 'ir.config_parameter',
                method: 'search_read',
                domain: [['key', '=like', 'app_%']],
                fields: ['key', 'value'],
                lazy: false,
            }).then(function (res) {
                $.each(res, function (key, val) {
                    if (session.user_context.uid!=1 || (val.key == 'app_show_debug' && val.value == "False")) {
                        $('[data-menu="debug"]').parent().hide();
                        $('[data-menu="debugassets"]').parent().hide();
                        $('[data-menu="quitdebug"]').parent().hide();
                    }
                });
            })
        },
        /**
         * @override
         */
        start: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                var mMode = 'normal';
                if (window.location.href.indexOf('debug') != -1)
                    mMode = 'debug';
                if (window.location.href.indexOf('debug=assets') != -1)
                    mMode = 'assets';
                if (mMode == 'normal')
                    $('[data-menu="quitdebug"]').parent().hide();
                if (mMode == 'debug')
                    $('[data-menu="debug"]').parent().hide();
                if (mMode == 'assets')
                    $('[data-menu="debugassets"]').parent().hide();
            });
        },
        _onMenuDebug: function () {
            window.location = $.param.querystring(window.location.href, 'debug');
        },
        _onMenuDebugassets: function () {
            window.location = $.param.querystring(window.location.href, 'debug=assets');
        },
        _onMenuQuitdebug: function () {
            window.location.search = "?";
        },
    })

});
