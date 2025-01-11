from odoo import fields, models


class AccountPayment(models.Model):
    _inherit = "account.payment"

    payee_override = fields.Char(string="Payee Override", help="Override Payee Name on Check")
    
    check_date_override = fields.Date(
        string="Check Date",
        default=fields.Date.context_today,
        copy=True,
    )