# -*- coding: utf-8 -*-
{
    'name': "kd_mrp_choose_production_location",

    'summary': """
        Module for Set Production location in Operation """,

    'description': """
        Module for Set Production location in Operation
    """,

    'author': "Khmerdev",
    'website': "http://www.khmerdev.com",
    'license': "AGPL-3",
    # Category:
    # Human Resources, Industries, Localization, Manufacturing, Marketing, Point of Sale ,Productivity, Project, Purchases
    # Sales, Warehouse, Website, Extra Tools
    'category': 'Manufacturing',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','stock','mrp'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/stock_picking_type_views.xml',
        'views/mrp_production_form.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
}