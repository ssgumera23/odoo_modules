from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "purchase.order"
    total_purchase_qty = fields.Float(string="Total Qty", compute='_get_total_qty')

    @api.depends('order_line.product_qty')
    def _get_total_qty(self):
        for order in self:
            order.total_purchase_qty = sum(order.order_line.mapped('product_qty'))
