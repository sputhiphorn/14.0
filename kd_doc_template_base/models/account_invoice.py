
from odoo import api, models, fields, _
from odoo.exceptions import Warning



class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    currency_rate_khmer = fields.Float(string="Currency Rate Khmer", compute='_compute_currency_khmer')
    currency_symbol_khmer = fields.Char(string="Currency Symbol Khmer", compute='_compute_currency_khmer')
    amount_total_khmer = fields.Float(string='Amount In Khmer', readonly=True, compute='_compute_currency_khmer')

    @api.one
    def _compute_currency_khmer(self):
        currency_khmer = self.env['res.currency'].search([('name', '=', 'KHR')], limit=1)
        self.currency_rate_khmer = currency_khmer.rate
        self.currency_symbol_khmer = currency_khmer.symbol
        self.amount_total_khmer = float(self.amount_total) * self.currency_rate_khmer

    def check_invoice_journal(self):
        try:
            if self.type == 'out_invoice':
                sequence_tax_withouttax = self.env['ir.config_parameter'].sudo().get_param('kd_invoice-sequence-tax-withouttax.sequence_tax_withouttax')
                sequence_tax_withouttax_by_warehouse = self.env['ir.config_parameter'].sudo().get_param('kd_invoice-sequence-tax-withouttax.sequence_tax_withouttax_by_warehouse')
                if sequence_tax_withouttax == 'True':
                    pid = self.env['res.partner']._find_accounting_partner(self.partner_id).id
                    view = self.env['res.partner'].search([('id', '=', pid)], limit=1)
                    tax = super(AccountInvoice, self)._get_tax_amount_by_group()
                    journal_tax_id = int(self.env['ir.config_parameter'].sudo().get_param('kd_invoice-sequence-tax-withouttax.journal_tax_id'))
                    journal_withouttax_id = int(self.env['ir.config_parameter'].sudo().get_param('kd_invoice-sequence-tax-withouttax.journal_withouttax_id'))
                    if not view.vat:
                        self.journal_id = journal_withouttax_id
                    else:
                        self.journal_id = journal_tax_id
                elif sequence_tax_withouttax_by_warehouse == 'True':
                    if len(self.partner_id.warehouse_id._ids) == 0:
                        raise Warning(_("Cannot find invoice journals for warehouse. You Should Configure it. Please go to Account Configuration."))
                    else:
                        commercial_invoice = self.env['kd_doc_template_base.commercial_invoice'].search(
                            [('warehouse_id', '=', self.partner_id.warehouse_id.id)], limit=1)
                        if len(commercial_invoice) == 0:
                            raise Warning(_("Cannot find invoice journals for warehouse. You Should Configure it. Please go to Account Configuration."))
                        else:
                            tax = super(AccountInvoice, self)._get_tax_amount_by_group()
                            if not tax:
                                self.journal_id = int(commercial_invoice.journal_withouttax_id.id)
                            else:
                                self.journal_id = int(commercial_invoice.journal_tax_id.id)
        except:
            raise Warning(_("Cannot find invoice journals for warehouse. You Should Configure it. Please go to Account Configuration."))
        return

    @api.multi
    def action_invoice_open(self):
        self.check_invoice_journal()
        super(AccountInvoice, self).action_invoice_open()