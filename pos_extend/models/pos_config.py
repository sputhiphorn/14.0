# -*- coding: utf-8 -*-
from odoo import fields, models, _


class pos_config(models.Model):
    _inherit = "pos.config"

    # Multi Currency
    multi_currency = fields.Boolean('Multi currency', default=0)
