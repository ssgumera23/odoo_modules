# Copyright 2020 Tech Ops PH
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Check Printing Report PH",
    "summary": "Print Checks (as Reports) from Vouchers",
    "description": """
        Philippines Check
        PH Check Format
        check print
        check printing
        check printing ph
        check printing philippines
        check printing report ph
        pchc
        philippine clearing house corporation
        check clearing format
        check clearing
        check design
        new check design
        clearing officers of banks
        
    """,
    "version": "16.0.1.0.1",
    "price": "108.00",
    "currency": "USD",
    "license": "AGPL-3",
    "author": "Tech Ops PH, "
              "EL Abquina",
    "category": "Generic Modules/Accounting",
    "website": "https://techops.ph",
    "depends": ["account_check_printing"],
    "data": [
        "data/report_paperformat.xml",
        "data/ir_actions_report.xml",
        "views/res_company.xml",
        "report/action_report_check_ph.xml",
        "report/report_check_ph.xml",
        "report/print_check_ph.xml",
        "report/layout_dates.xml",
        "report/layout_parts.xml",
        "report/layout_print_check_ph.xml",
    ],
    "installable": True,
    "images": ["static/src/check_printing_report_ph.jpg", "static/src/check_printing_report_ph_screenshot.jpg"],
}

