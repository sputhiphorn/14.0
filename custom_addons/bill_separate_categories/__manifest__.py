# -*- coding: utf-8 -*-
{
    'name': 'KD_Kitchen_Separate_by_Category',
    'summary': """POS Extend Function for separate product in bill""",
    'version': '11.0.1.0',
    'description': """POS Extend Function for separate product in bill""",
    'author': 'KhmerDev',
    'company': 'KhmerDev',
    'website': 'http://www.khmerdev.com',
    'category': 'Point of Sale',
    'depends': ['base', 'point_of_sale', 'pos_restaurant'],
    'license': 'OPL-1',
    'data': [
    	'views/kitchen_ticket_template.xml',
        'views/pos_config.xml'
    ],
    'qweb': ['static/src/xml/kitchen_ticket.xml',],
    'images': [],
    'demo': [],        
    'installable': True,
    'application': True,
    'auto_install': False,

}
