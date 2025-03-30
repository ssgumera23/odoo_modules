# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _

class AccountReport(models.Model):
    _inherit = 'account.report'

    # filter_salesperson = None

    filter_salesperson = fields.Boolean(
        string="Sales Persons",
        compute=lambda x: x._compute_report_option_filter('filter_salesperson'), readonly=False, store=True, depends=['root_report_id'],
    )

    @api.model
    def _init_options_salesperson(self, options, previous_options=None):
        if not self.filter_salesperson:
            return
        options['salesperson'] = True
        options['salesperson_ids'] = previous_options and previous_options.get('salesperson_ids') or []
        selected_salesperson_ids = [int(partner) for partner in options['salesperson_ids']]
        selected_salespersons = selected_salesperson_ids and self.env['res.users'].browse(selected_salesperson_ids) or self.env[
            'res.users']
        options['selected_salesperson_ids'] = selected_salespersons.mapped('name')

    @api.model
    def _get_options_salesperson_domain(self, options):
        domain = []
        if options.get('salesperson_ids'):
            salesperson_ids = [int(salesperson) for salesperson in options['salesperson_ids']]
            domain.append(('partner_id.user_id', 'in', salesperson_ids))
        return domain

    @api.model
    def _get_options_domain(self, options, date_scope):
        # OVERRIDE
        # Handle filter_unreconciled + filter_account_type
        domain = super(AccountReport, self)._get_options_domain(options, date_scope)
        domain += self._get_options_salesperson_domain(options)
        return domain