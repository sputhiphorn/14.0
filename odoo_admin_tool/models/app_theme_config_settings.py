# -*- coding: utf-8 -*-

import logging

from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    _description = u"Odoo Tool"
    app_system_name = fields.Char('System Name', help=u"Setup System Name,which replace Odoo")
    app_show_debug = fields.Boolean('Show Quick Debug', help=u"When enable,everyone login can see the debug menu")

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        ir_config = self.env['ir.config_parameter'].sudo()
        app_system_name = ir_config.get_param('app_system_name', default='Odoo')
        app_show_debug = True if ir_config.get_param('app_show_debug') == "True" else False
        res.update(
            app_system_name=app_system_name,
            app_show_debug=app_show_debug,
        )
        return res

    @api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        ir_config = self.env['ir.config_parameter']
        ir_config.set_param("app_system_name", self.app_system_name or "")
        ir_config.set_param("app_show_debug", self.app_show_debug or "False")

    @api.multi
    def remove_sales(self):
        to_removes = [
            ['sale.order.line', ],
            ['sale.order', ],
        ]
        try:
            for line in to_removes:
                obj_name = line[0]
                obj = self.pool.get(obj_name)
                if obj:
                    sql = "delete from %s" % obj._table
                    self._cr.execute(sql)
            seqs = self.env['ir.sequence'].search([('code', '=', 'sale.order')])
            for seq in seqs:
                seq.write({
                    'number_next': 1,
                })
            sql = "update ir_sequence set number_next=1 where code ='sale.order';"
            self._cr.execute(sql)
        except Exception as e:
            raise Warning(e)
        return True

    def remove_product(self):
        to_removes = [
            ['product.product', ],
            ['product.template', ],
        ]
        try:
            for line in to_removes:
                obj_name = line[0]
                obj = self.pool.get(obj_name)
                if obj:
                    sql = "delete from %s" % obj._table
                    self._cr.execute(sql)
            seqs = self.env['ir.sequence'].search([('code', '=', 'product.product')])
            for seq in seqs:
                seq.write({
                    'number_next': 1,
                })
            sql = "update ir_sequence set number_next=1 where code ='product.product';"
            self._cr.execute(sql)
        except Exception as e:
            pass
        return True

    def remove_product_attribute(self):
        to_removes = [
            ['product.attribute.value', ],
            ['product.attribute', ],
        ]
        try:
            for line in to_removes:
                obj_name = line[0]
                obj = self.pool.get(obj_name)
                if obj:
                    sql = "delete from %s" % obj._table
                    self._cr.execute(sql)
        except Exception as e:
            pass
        return True

    @api.multi
    def remove_pos(self):
        to_removes = [
            ['pos.order.line', ],
            ['pos.order', ],
        ]
        try:
            for line in to_removes:
                obj_name = line[0]
                obj = self.pool.get(obj_name)
                if obj:
                    sql = "delete from %s" % obj._table
                    self._cr.execute(sql)
            seqs = self.env['ir.sequence'].search([('code', '=', 'pos.order')])
            for seq in seqs:
                seq.write({
                    'number_next': 1,
                })
            sql = "update ir_sequence set number_next=1 where code ='pos.order';"
            self._cr.execute(sql)
        except Exception as e:
            pass
        return True

    @api.multi
    def remove_purchase(self):
        to_removes = [
            ['purchase.order.line', ],
            ['purchase.order', ],
            ['purchase.requisition.line', ],
            ['purchase.requisition', ],
        ]
        try:
            for line in to_removes:
                obj_name = line[0]
                obj = self.pool.get(obj_name)
                if obj:
                    sql = "delete from %s" % obj._table
                    self._cr.execute(sql)
            seqs = self.env['ir.sequence'].search([('code', '=', 'purchase.order')])
            for seq in seqs:
                seq.write({
                    'number_next': 1,
                })
            sql = "update ir_sequence set number_next=1 where code ='purchase.order';"
            self._cr.execute(sql)
        except Exception as e:
            pass
        return True

    @api.multi
    def remove_mrp(self):
        to_removes = [
            ['mrp.workcenter.productivity', ],
            ['mrp.workorder', ],
            ['mrp.production.workcenter.line', ],
            ['change.production.qty', ],
            ['mrp.production', ],
            ['mrp.production.product.line', ],
            ['mrp.unbuild', ],
            ['change.production.qty', ],
            ['sale.forecast.indirect', ],
            ['sale.forecast', ],
        ]
        try:
            for line in to_removes:
                obj_name = line[0]
                obj = self.pool.get(obj_name)
                if obj:
                    sql = "delete from %s" % obj._table
                    self._cr.execute(sql)
            seqs = self.env['ir.sequence'].search(['|', ('code', '=', 'mrp.production'), ('code', '=', 'mrp.unbuild')])
            for seq in seqs:
                seq.write({
                    'number_next': 1,
                })
            sql = "update ir_sequence set number_next=1 where (code ='mrp.production' or code ='mrp.unbuild');"
            self._cr.execute(sql)
        except Exception as e:
            pass
        return True

    @api.multi
    def remove_mrp_bom(self):
        to_removes = [
            ['mrp.bom.line', ],
            ['mrp.bom', ],
        ]
        try:
            for line in to_removes:
                obj_name = line[0]
                obj = self.pool.get(obj_name)
                if obj:
                    sql = "delete from %s" % obj._table
                    self._cr.execute(sql)
        except Exception as e:
            pass
        return True

    @api.multi
    def remove_inventory(self):
        to_removes = [
            ['stock.quant', ],
            ['stock.quant.package', ],
            ['stock.quant.move.rel', ],
            ['stock.move.line', ],
            ['stock.move', ],
            ['stock.pack.operation', ],
            ['stock.picking', ],
            ['stock.scrap', ],
            ['stock.inventory.line', ],
            ['stock.inventory', ],
            ['stock.production.lot', ],
            ['stock.fixed.putaway.strat', ],
            ['make.procurement', ],
            ['procurement.order', ],
            ['procurement.group', ],
        ]
        try:
            for line in to_removes:
                obj_name = line[0]
                obj = self.pool.get(obj_name)
                if obj:
                    sql = "delete from %s" % obj._table
                    self._cr.execute(sql)
            seqs = self.env['ir.sequence'].search([
                '|', ('code', '=', 'stock.lot.serial'),
                '|', ('code', '=', 'stock.lot.tracking'),
                '|', ('code', '=', 'stock.orderpoint'),
                '|', ('code', '=', 'stock.picking'),
                '|', ('code', '=', 'stock.quant.package'),
                '|', ('code', '=', 'stock.scrap'),
                '|', ('code', '=', 'stock.picking'),
                '|', ('prefix', '=', 'WH/IN/'),
                '|', ('prefix', '=', 'WH/INT/'),
                '|', ('prefix', '=', 'WH/OUT/'),
                '|', ('prefix', '=', 'WH/PACK/'),
                ('prefix', '=', 'WH/PICK/')
            ])

            for seq in seqs:
                seq.write({
                    'number_next': 1,
                })
            sql = "update ir_sequence set number_next=1 where (" \
                  "code ='stock.lot.serial' " \
                  "or code ='stock.lot.tracking' " \
                  "or code ='stock.orderpoint'" \
                  "or code ='stock.picking'" \
                  "or code ='stock.quant.package'" \
                  "or code ='stock.scrap'" \
                  "or code ='stock.picking'" \
                  "or prefix ='WH/IN/'" \
                  "or prefix ='WH/INT/'" \
                  "or prefix ='WH/OUT/'" \
                  "or prefix ='WH/PACK/'" \
                  "or prefix ='WH/PICK/'" \
                  ");"
            self._cr.execute(sql)
        except Exception as e:
            pass
        return True

    @api.multi
    def remove_account(self):
        to_removes = [
            ['account.voucher.line', ],
            ['account.voucher', ],
            ['account.bank.statement.line', ],
            ['account.bank.statement', ],
            ['account.payment', ],
            ['account.analytic.line', ],
            ['account.analytic.account', ],
            ['account.invoice.line', ],
            ['account.invoice.refund', ],
            ['account.invoice', ],
            ['account.partial.reconcile', ],
            ['account.move.line', ],
            ['hr.expense.sheet', ],
            ['account.move', ],
        ]
        try:
            for line in to_removes:
                obj_name = line[0]
                obj = self.pool.get(obj_name)
                if obj:
                    sql = "delete from %s" % obj._table
                    self._cr.execute(sql)

                    seqs = self.env['ir.sequence'].search([
                        '|', ('code', '=', 'account.reconcile'),
                        '|', ('code', '=', 'account.payment.customer.invoice'),
                        '|', ('code', '=', 'account.payment.customer.refund'),
                        '|', ('code', '=', 'account.payment.supplier.invoice'),
                        '|', ('code', '=', 'account.payment.supplier.refund'),
                        '|', ('code', '=', 'account.payment.transfer'),
                        '|', ('prefix', 'like', 'BNK1/'),
                        '|', ('prefix', 'like', 'CSH1/'),
                        '|', ('prefix', 'like', 'INV/'),
                        '|', ('prefix', 'like', 'EXCH/'),
                        '|', ('prefix', 'like', 'MISC/'),
                        '|', ('prefix', 'like', u'Bill/'),
                        ('prefix', 'like', u'Miscellaneous/')
                    ])

                    for seq in seqs:
                        seq.write({
                            'number_next': 1,
                        })
                    sql = "update ir_sequence set number_next=1 where (" \
                          "code ='account.reconcile' " \
                          "or code ='account.payment.customer.invoice' " \
                          "or code ='account.payment.customer.refund' " \
                          "or code ='account.payment.supplier.invoice' " \
                          "or code ='account.payment.supplier.refund' " \
                          "or prefix like 'BNK1/%'" \
                          "or prefix like 'CSH1/%'" \
                          "or prefix like 'INV/%'" \
                          "or prefix like 'EXCH/%'" \
                          "or prefix like 'MISC/%'" \
                          "or prefix like 'Bill/%'" \
                          "or prefix like 'Miscellaneous/%'" \
                          ");"
                    self._cr.execute(sql)
        except Exception as e:
            pass
        return True

    @api.multi
    def remove_account_chart(self):
        to_removes = [
            ['account.tax.account.tag', ],
            ['account.tax', ],
            ['account.account.account.tag', ],
            ['wizard_multi_charts_accounts'],
            ['account.account', ],
            ['account.journal', ],
        ]
        try:
            for line in to_removes:
                obj_name = line[0]
                obj = self.pool.get(obj_name)
                if obj:
                    sql = "delete from %s" % obj._table
                    self._cr.execute(sql)
            field1 = self.env['ir.model.fields']._get('product.template', "taxes_id").id
            field2 = self.env['ir.model.fields']._get('product.template', "supplier_taxes_id").id

            sql = ("delete from ir_default where field_id = %s or field_id = %s") % (field1, field2)
            self._cr.execute(sql)

            sql = "update res_company set chart_template_id=null ;"
            self._cr.execute(sql)
        except Exception as e:
            pass
        return True

    @api.multi
    def remove_project(self):
        to_removes = [
            ['account.analytic.line', ],
            ['project.task', ],
            ['project.forecast', ],
            ['project.project', ],
        ]
        try:
            for line in to_removes:
                obj_name = line[0]
                obj = self.pool.get(obj_name)
                if obj:
                    sql = "delete from %s" % obj._table
                    self._cr.execute(sql)
        except Exception as e:
            pass
        return True

    @api.multi
    def remove_message(self):
        to_removes = [
            ['mail.message', ],
            ['mail.followers', ],
        ]
        try:
            for line in to_removes:
                obj_name = line[0]
                obj = self.pool.get(obj_name)
                if obj and obj._table:
                    sql = "delete from %s" % obj._table
                    self._cr.execute(sql)
        except Exception as e:
            pass
        return True

    @api.multi
    def remove_workflow(self):
        to_removes = [
            ['wkf.workitem', ],
            ['wkf.instance', ],
        ]
        try:
            for line in to_removes:
                obj_name = line[0]
                obj = self.pool.get(obj_name)
                if obj and obj._table:
                    sql = "delete from %s" % obj._table
                    self._cr.execute(sql)

        except Exception as e:
            pass
        return True

    @api.multi
    def remove_all_biz(self):
        try:
            self.remove_account()
            self.remove_inventory()
            self.remove_mrp()
            self.remove_purchase()
            self.remove_sales()
            self.remove_project()
            self.remove_message()
        except Exception as e:
            pass
        return True
