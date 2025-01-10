from odoo import fields, models, api
from odoo.addons.base.models.decimal_precision import dp


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
    discount_amount = fields.Float(string="Discount Amount", digits=dp.get_precision('Product Price'))

    @api.onchange("discount_amount")
    def compute_discount_amount(self):
        if self.price_unit:
            self.discount = (self.discount_amount / (self.price_unit * self.product_uom_qty)) * 100

    @api.onchange("discount")
    def compute_discount_percentage(self):
        if self.price_unit:
            self.discount_amount = (self.product_uom_qty * self.price_unit) * (self.discount / 100)

