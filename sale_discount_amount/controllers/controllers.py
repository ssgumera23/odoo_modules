# -*- coding: utf-8 -*-
# from odoo import http


# class SaleDiscountAmount(http.Controller):
#     @http.route('/sale_discount_amount/sale_discount_amount', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sale_discount_amount/sale_discount_amount/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sale_discount_amount.listing', {
#             'root': '/sale_discount_amount/sale_discount_amount',
#             'objects': http.request.env['sale_discount_amount.sale_discount_amount'].search([]),
#         })

#     @http.route('/sale_discount_amount/sale_discount_amount/objects/<model("sale_discount_amount.sale_discount_amount"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sale_discount_amount.object', {
#             'object': obj
#         })
