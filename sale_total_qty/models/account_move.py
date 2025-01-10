from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"
    total_inv_qty = fields.Float(string="Total Qty", compute='_get_total_qty')
    total_sales_vat_inc = fields.Float(string="Total Sales VAT Inc", compute='_get_tsvi')

    @api.depends('invoice_line_ids.quantity')
    def _get_total_qty(self):
        for order in self:
            order.total_inv_qty = sum(order.invoice_line_ids.mapped('quantity'))

    def _get_tsvi(self):
        self.total_sales_vat_inc = self.amount_untaxed + self.amount_tax