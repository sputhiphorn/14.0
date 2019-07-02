# -*- coding: utf-8 -*-
{
    'name': 'Odoo Admin Tool',
    'version': '11.19.1.20',
    'author': 'KhmerDev',
    'category': 'Tool',
    'website': 'http://www.khmerdev.com',
    'license': 'AGPL-3',
    'sequence': 2,
    'summary': """    
        Data clearing,Delete data.reset account chart.
    """,
    'description': """
        Data clearing,Delete data.reset account chart.
    """,
    'images': ['static/description/banner.gif'],
    'depends': ['base', 'web', 'mail'],
    'data': [
        'views/app_odoo_customize_view.xml',
        'views/app_theme_config_settings_view.xml',
        # data
        'data/ir_config_parameter.xml',
        'data/res_company_data.xml',
        'data/res_groups.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [],
    'test': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': [
        'static/src/xml/customize_user_menu.xml',
    ],
}
