# -*- coding: utf-8 -*-
# Copyright 2016-2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    "name": "Khmerdev Theme",
    "summary": "Theme For Khmerdev comapany "
               "web",
    "version": "11.0.1.0.2",
    "category": "Website",
    "website": "https://khmerdev.com/",
    "author": "Khmerdev",
    "license": "LGPL-3",
    "installable": True,
    "depends": [
        'web',
    ],
    "data": [
        'data/ir_config_parameter.xml',
        'views/website_templates.xml',
        'views/assets.xml',
        'views/res_company_view.xml',
        'views/res_users_view.xml',
        'views/web.xml',
        'views/web_login.xml',
    ],
    'qweb': [
        'static/src/xml/form_view.xml',
        'static/src/xml/navbar.xml',
    ],
}
