# -*- coding: utf-8 -*-
{
    'name': 'POS Extend Function',
    'summary': """POS Extend Function for global discount""",
    'version': '11.0.1.0',
    'description': """POS Extend Function for global discount""",
    'author': 'KhmerDev',
    'company': 'KhmerDev',
    'website': 'http://www.khmerdev.com',
    'category': 'Point of Sale',
    'depends': ['pos_extend'],
    'data':[
        'views/pos_discount_extend_template.xml',
    ],
    'license': 'OPL-1',
    'qweb': ['static/src/xml/*.xml',],
    'demo': [],        
    'installable': True,
    'application': True,
    'auto_install': False,

}