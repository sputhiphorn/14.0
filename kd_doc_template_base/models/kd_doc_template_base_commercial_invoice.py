# -*- coding: utf-8 -*-

from odoo import models, fields


class KDCommercialInvoice(models.Model):
    _name = 'kd_doc_template_base.commercial_invoice'
    _description = 'Commercial Invoice'

    warehouse_id = fields.Many2one('stock.warehouse', 'Warehouse', required=True)
    journal_tax_id = fields.Many2one('account.journal', string='Tax Invoice ', domain=[('type', '=', 'sale')], required=True)
    journal_withouttax_id = fields.Many2one('account.journal', string='Commercial Invoice ', domain=[('type', '=', 'sale')], required=True)