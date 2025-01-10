from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"
    total_sale_qty = fields.Float(string="Total Qty", compute='_get_total_qty')
    total_sales_vat_inc = fields.Float(string="Total Sales VAT Inc", compute='_get_tsvi')

    @api.depends('order_line.product_uom_qty')
    def _get_total_qty(self):
        for order in self:
            order.total_sale_qty = sum(order.order_line.mapped('product_uom_qty'))

    def _get_tsvi(self):
        self.total_sales_vat_inc = self.amount_untaxed + self.amount_tax
