# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class PickingType(models.Model):
    _inherit = "stock.picking.type"

    production_location_id = fields.Many2one(
        string='Production Location',
        comodel_name='stock.location',
    )