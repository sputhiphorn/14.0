# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
import base64
import json
import logging

_logger = logging.getLogger(__name__)

class pos_order(models.Model):
    _inherit = "pos.order"
    
    ean13 = fields.Char('Ean13')
    exchange_rate = fields.Float(string='Exchange Rate')

    @api.model
    def _order_fields(self, ui_order):
        order_fields = super(pos_order, self)._order_fields(ui_order)
        
        if ui_order.get('ean13', False):
            order_fields.update({
                'ean13': ui_order['ean13']
            })
        if ui_order.get('exchange_rate', False):
            order_fields.update({
                'exchange_rate': ui_order['exchange_rate']
            })
        return order_fields


class exchange_rate(models.Model):
    _inherit = "res.currency"

    @api.model
    def get_convert_rate(self, currency_code):
        rate = 1
        t_currency = self.env['res.currency'].search([('name', '=ilike', currency_code)], limit=1)
        if t_currency:
            rate = t_currency.rate
        return {"rate": rate}

class ReportSaleDetails_Inherit(models.AbstractModel):
    _inherit = "report.point_of_sale.report_saledetails"

    @api.model
    def get_sale_details(self, date_start=False, date_stop=False, configs=False):
        recode = super(ReportSaleDetails_Inherit, self).get_sale_details(date_start, date_stop, configs)
        recode.update({'label_sale_detail': _('Sales Details'),
                       'label_products': _('Products'),
                       'label_product': _('Product'),
                       'label_quantity': _('Quantity'),
                       'label_price_unit': _('Price Unit'),
                       'label_total': _('Total'),
                       'label_payments': _('Payments'),
                       'label_name': _('Name'),
                       'label_taxes': _('Taxes'),
                       'label_tax_amount': _('Tax Amount'),
                       'label_base_amount': _('Base Amount'),
                       'label_disc': _('Disc: ')
                       })
        return recode
