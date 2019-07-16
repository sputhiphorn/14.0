# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sequence_tax_withouttax = fields.Boolean("Invoice Tax and Commercial Invoice")
    journal_tax_id = fields.Many2one('account.journal', string='Tax Invoice ', domain=[('type', '=', 'sale')])
    journal_withouttax_id = fields.Many2one('account.journal', string='Commercial Invoice ', domain=[('type', '=', 'sale')])

    sequence_tax_withouttax_by_warehouse = fields.Boolean("Invoice Tax and Commercial Invoice By Warehouse")
    @api.multi
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            sequence_tax_withouttax=self.env['ir.config_parameter'].sudo().get_param('kd_invoice-sequence-tax-withouttax.sequence_tax_withouttax'),
            journal_tax_id=int(self.env['ir.config_parameter'].sudo().get_param('kd_invoice-sequence-tax-withouttax.journal_tax_id')),
            journal_withouttax_id=int(self.env['ir.config_parameter'].sudo().get_param('kd_invoice-sequence-tax-withouttax.journal_withouttax_id')),
            sequence_tax_withouttax_by_warehouse=self.env['ir.config_parameter'].sudo().get_param('kd_invoice-sequence-tax-withouttax.sequence_tax_withouttax_by_warehouse')
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('kd_invoice-sequence-tax-withouttax.sequence_tax_withouttax', self.sequence_tax_withouttax)
        self.env['ir.config_parameter'].sudo().set_param('kd_invoice-sequence-tax-withouttax.journal_tax_id', self.journal_tax_id.id)
        self.env['ir.config_parameter'].sudo().set_param('kd_invoice-sequence-tax-withouttax.journal_withouttax_id', self.journal_withouttax_id.id)
        self.env['ir.config_parameter'].sudo().set_param('kd_invoice-sequence-tax-withouttax.sequence_tax_withouttax_by_warehouse', self.sequence_tax_withouttax_by_warehouse)

    @api.onchange('sequence_tax_withouttax')
    def onchange_sequence_tax_withouttax(self):
        if self.sequence_tax_withouttax == True:
            self.sequence_tax_withouttax_by_warehouse = False

    @api.onchange('sequence_tax_withouttax_by_warehouse')
    def onchange_sequence_tax_withouttax_by_warehouse(self):
        if self.sequence_tax_withouttax_by_warehouse == True:
            self.sequence_tax_withouttax = False