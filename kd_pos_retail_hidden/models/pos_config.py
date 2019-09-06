# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
import base64
import json
import logging

_logger = logging.getLogger(__name__)

class pos_config(models.Model):
    _inherit = "pos.config"

    allow_lock_button = fields.Boolean('Show Lock Screen Button', default=0)
    allow_report_button = fields.Boolean('Show Report Button', default=0)
    allow_sync_data = fields.Boolean('Show Sync Data Button', default=0)
    allow_show_list = fields.Boolean('Show Product List View Button', default=0)
    allow_delete = fields.Boolean('Show Remove Order Blank Line Button', default=0)

    allow_remove_pos_cache = fields.Boolean('Show Remove Pos Cache Button', default=0)
    allow_sync_orders = fields.Boolean('Show Sync Orders Button', default=0)
    allow_combo_item_add_lot = fields.Boolean('Show Combo Item Add Lot Button', default=0)
    allow_set_seller = fields.Boolean('Show Set Seller Button', default=0)
    allow_set_fiscal_position = fields.Boolean('Show Set Fiscal Position Button', default=0)

