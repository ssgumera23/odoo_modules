# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class CustomResUsers(models.Model):
    _inherit = 'res.users'

    allowed_location_ids = fields.Many2many(string="Allowed Locations", comodel_name="stock.location", store=True)
