from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"
    total_stock_quantity = fields.Float(string="Total Quantity", compute='_get_total_qty')

    @api.depends('move_ids_without_package.product_uom_qty')
    def _get_total_qty(self):
        for order in self:
            order.total_stock_quantity = sum(order.mapped('move_ids_without_package.product_uom_qty'))


