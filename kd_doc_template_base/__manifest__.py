# -*- coding: utf-8 -*-
{
    'name': "kd_doc_template_base",

    'summary': """
        Customizable Report Template Invoice""",

    'description': """
        Customizable Report Template Invoice
        It can check invoice with tax and without tax.
    """,
    'license':'OPL-1',
    'author': "KhmerDev",
    'website': "http://www.khmerdev.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','base_vat','account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/kd_doc_template_base_commercial_invoice_view.xml',
        'views/custom_views.xml',
        'views/templates.xml',
        'reports/custom_report_layout.xml',
        'reports/sale_doc/custom_report_invoice_doc.xml',
        'views/res_config_settings_views.xml'
    ],
}