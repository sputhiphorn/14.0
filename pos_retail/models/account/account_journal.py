# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class account_journal(models.Model):
    _inherit = "account.journal"

    voucher = fields.Boolean('Voucher', help='This is account journal give all transactions of customers use voucher')
    credit = fields.Boolean('Credit card', help="Journal use for customer's credit card")

    pos_method_type = fields.Selection([
        ('default', 'Default'),
        ('rounding', 'Rounding'),
        ('wallet', 'Wallet'),
        ('voucher', 'Voucher'),
        ('credit', 'Credit/Debt'),
        ('return', 'Return Order')
    ], default='default', string='POS method type', required=1)

    decimal_rounding = fields.Integer('Decimal rounding', default=1, help='Example: Amount total is 1.94, set rounding 1, amount total will covert to 1.9, if set rounding 0 amount total will covert to 2.0')




