# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    @api.multi
    def _generate_moves(self):
        if self.picking_type_id.production_location_id:
            self.production_location_id = self.picking_type_id.production_location_id
        return super(MrpProduction,self)._generate_moves()