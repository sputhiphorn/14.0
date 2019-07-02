# -*- coding: utf-8 -*-
{
    'name': 'POS Extend Function',
    'summary': """POS Extend Function for language name field""",
    'version': '11.0.1.0',
    'description': """POS Extend Function for language name field""",
    'author': 'KhmerDev',
    'company': 'KhmerDev',
    'website': 'http://www.khmerdev.com',
    'category': 'Point of Sale',
    'depends': ['base', 'point_of_sale','product'],
    'license': 'OPL-1',
    'data': [
        'views/product_views.xml',
        'views/posticket_template.xml',
    ],
    'qweb': ['static/src/xml/posticket.xml',],
    'images': [],
    'demo': [],        
    'installable': True,
    'application': True,
    'auto_install': False,

}