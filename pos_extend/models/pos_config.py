# -*- coding: utf-8 -*-
from odoo import fields, models, _


class pos_config(models.Model):
    _inherit = "pos.config"

    # Multi Currency
    multi_currency = fields.Boolean('Multi currency', default=0)
    multi_currency_update_rate = fields.Boolean('Update rate', default=0)