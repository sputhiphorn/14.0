# -*- coding: utf-8 -*-
{
    'name': 'POS Extend Function',
    'summary': """POS Extend Function""",
    'version': '11.0.1.0',
    'description': """POS Extend Function""",
    'author': 'KhmerDev',
    'company': 'KhmerDev',
    'website': 'http://www.khmerdev.com',
    'category': 'Point of Sale',
    'depends': ['point_of_sale', 'pos_retail'],
    'license': 'OPL-1',
    'data': [
    	'views/register.xml',
    	'views/pos_order.xml',
        'views/inherit_report_saledetails.xml'
    ],
    'qweb': ['static/src/xml/*.xml',],
    'images': ['static/description/banner.png'],
    'demo': [],        
    'installable': True,
    'application': True,
    'auto_install': False,

}
