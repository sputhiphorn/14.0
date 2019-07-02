from odoo import api, fields, models, _

class ProductTemplate(models.Model):
    _inherit = "product.template"

    other_language_name = fields.Char()