# -*- coding: utf-8 -*-
from odoo import models, fields

class res_company(models.Model):
    _inherit = "res.company"
    external_report_layout = fields.Selection([
            ('background', 'Background'),
            ('boxed', 'Boxed'),
            ('clean', 'Clean'),
            ('standard', 'Standard'),
            ('custom', 'Custom'),
        ], string='Document Template')
    report_logo = fields.Binary(string="Report Logo")