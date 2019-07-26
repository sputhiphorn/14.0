# -*- coding: utf-8 -*-
# This module open source
# Design and development by: KhmerDev (chanthou.pring@gmail.com)

from odoo import api, fields, models

class PosConfig_Inherit(models.Model):
    _inherit = "pos.config"

    separate_category = fields.Boolean('Adding Separate Category To Menu of Receipt')