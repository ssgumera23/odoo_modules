# -*- coding: utf-8 -*-
# from odoo import http


# class SaleTotalQty(http.Controller):
#     @http.route('/sale_total_qty/sale_total_qty', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sale_total_qty/sale_total_qty/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sale_total_qty.listing', {
#             'root': '/sale_total_qty/sale_total_qty',
#             'objects': http.request.env['sale_total_qty.sale_total_qty'].search([]),
#         })

#     @http.route('/sale_total_qty/sale_total_qty/objects/<model("sale_total_qty.sale_total_qty"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sale_total_qty.object', {
#             'object': obj
#         })
