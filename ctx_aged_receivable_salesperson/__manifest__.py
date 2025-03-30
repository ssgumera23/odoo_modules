{
    'name': 'Aged Receivable Report per salesperson',
    'version': '1.0.2',
    'category': 'Accounting',
    'summary': 'Aged Receivable Report per salesperson',
    'description': """ Aged Receivable Report per salesperson
    """,
    'author': 'CorTex IT Solutions Ltd.',
    'website': 'https://cortexsolutions.net',
    'license': 'OPL-1',
    'currency': 'EUR',
    'price': 50,
    'support': 'support@cortexsolutions.net',
    'depends': ['account_reports'],
    "data": [
        'data/accounts_report_data.xml',
        'data/accounts_report_column.xml',
        'views/search_template_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            '/ctx_aged_receivable_salesperson/static/src/js/account_reports.js',
        ],
    },
    'images': ['static/description/main_screenshot.png'],
    'installable': True,
    'auto_install': False,
}
