from odoo import models, fields


class Company(models.Model):
    _inherit = "res.company"

    # here, key has to be full xmlID(including the module name) of all the
    # new report actions that you have defined for check layout
    account_check_printing_layout = fields.Selection(selection_add=[
        ('account_check_printing_report_ph.action_report_check_ph', 'PH Bank Check'),
        ('account_check_printing_report_ph.action_report_check_ph_corp', 'PH Bank Check - Corporate'),
    ], ondelete={
        'account_check_printing_report_ph.action_report_check_ph': 'set default',
        'account_check_printing_report_ph.action_report_check_ph_corp': 'set default',
    },
    default='account_check_printing_report_ph.action_report_check_ph'
    )
