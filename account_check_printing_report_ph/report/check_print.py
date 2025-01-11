from odoo import api, models
from odoo.tools.safe_eval import safe_eval
from odoo.tools import float_is_zero
from fractions import Fraction

class ReportCheckPrint(models.AbstractModel):
    _name = "report.account_check_printing_report_ph.report_check_ph"
    _description = "Report Check Print - PH"

    @api.model
    def fill_stars_number(self, amount, stars_prefix=3, stars_suffix=3):
        str_prefix = " ".join(["*" * stars_prefix, amount, "*" * stars_suffix])
        return str_prefix

    def _format_date_to_partner_lang(self, date, partner_id):
        lang_code = self.env["res.partner"].browse(partner_id).lang
        lang = self.env["res.lang"]._lang_get(lang_code)
        return date.strftime(lang.date_format)

    @api.model
    def residual_PH(self, amount):
        str_amount = str("%.2f" % round(amount, 2)).split(".")
        check_residual_amt = "& " + str_amount[1] + "/100" 
        return check_residual_amt
        
    def amount2words_PH(self, amount_in_word):
        new_amount_in_word = amount_in_word.split("Peso")
        return new_amount_in_word[0].replace("And ", "").replace(",", "")
        
    def fill_stars(self, amount_in_word):
        if amount_in_word and len(amount_in_word) < 100:
            stars = 100 - len(amount_in_word)
            return " ".join([amount_in_word, "*" * stars])
        else:
            return amount_in_word

    def _get_residual_amount(self, payment, line):
        amt = line.amount_residual
        if amt < 0.0:
            amt *= -1
        amt = payment.company_id.currency_id.with_context(
            date=payment.date
        ).compute(amt, payment.currency_id)
        return amt

    def _get_total_amount(self, payment, line):
        amt = line.balance
        if amt < 0.0:
            amt *= -1
        amt = payment.company_id.currency_id.with_context(
            date=payment.date
        ).compute(amt, payment.currency_id)
        return amt

    def _get_paid_amount(self, payment, line):
        amount = 0.0
        total_amount_to_show = 0.0
        # We pay out
        if line.matched_credit_ids:
            amount = sum([p.amount for p in line.matched_credit_ids])
        # We receive payment
        elif line.matched_debit_ids:
            amount = sum([p.amount for p in line.matched_debit_ids])

        amount_to_show = payment.company_id.currency_id.with_context(
            date=payment.date
        ).compute(amount, payment.currency_id)
        if not float_is_zero(
            amount_to_show, precision_rounding=payment.currency_id.rounding
        ):
            total_amount_to_show = amount_to_show
        return total_amount_to_show

    def get_paid_lines(self, payments):
        lines = {}
        for payment in payments:
            lines[payment.id] = []
            pay_acc = (
                payment.journal_id.default_account_id
            )
            rec_lines = payment.line_ids.filtered(
                lambda x: x.account_id.reconcile and x.account_id != pay_acc
            )
            amls = rec_lines.mapped(
                "matched_credit_ids.credit_move_id"
            ) + rec_lines.mapped("matched_debit_ids.debit_move_id")
            amls -= rec_lines
            for aml in amls:
                date_due = aml.date_maturity
                total_amt = self._get_total_amount(payment, aml)
                residual_amt = self._get_residual_amount(payment, aml)
                paid_amt = self._get_paid_amount(payment, aml)
                line = {
                    "date_due": date_due,
                    "date": aml.date,
                    "reference": aml.display_name,
                    "number": aml.name,
                    "amount_total": total_amt,
                    "residual": residual_amt,
                    "paid_amount": paid_amt,
                }
                lines[payment.id].append(line)
        return lines

    @api.model
    def _get_report_values(self, docids, data=None):
        model = self.env.context.get("active_model", "account.payment")
        objects = self.env[model].browse(docids)
        paid_lines = self.get_paid_lines(objects)
        docargs = {
            "doc_ids": docids,
            "doc_model": model,
            "docs": objects,
            "fill_stars": self.fill_stars,
            "fill_stars_number": self.fill_stars_number,
            "paid_lines": paid_lines,
            "_format_date_to_partner_lang": self._format_date_to_partner_lang,
            "amount2words_PH": self.amount2words_PH,
            "residual_PH": self.residual_PH,
        }
        return docargs


class ReportCheckPrintCorp(models.AbstractModel):
    _name = "report.account_check_printing_report_ph.report_check_ph_corp"
    _inherit = "report.account_check_printing_report_ph.report_check_ph"
    _description = "Report Check Print for Corporate"


class ReportPrintCheckPH(models.AbstractModel):
    _name = "report.account_check_printing_report_ph.print_check_ph"
    _inherit = "report.account_check_printing_report_ph.report_check_ph"
    _description = "Report Check Print for Corporate"


class ReportPrintCheckPHCorp(models.AbstractModel):
    _name = "report.account_check_printing_report_ph.print_check_ph_corp"
    _inherit = "report.account_check_printing_report_ph.report_check_ph"
    _description = "Report Check Print for Corporate"