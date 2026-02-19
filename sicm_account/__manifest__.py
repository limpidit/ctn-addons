{
    'name': 'SICM Account',
    'version': '1.0',
    'description': 'SICM Account',
    'author': 'Limpid IT',
    'license': 'LGPL-3',
    'depends': [
        'sicm_base',
        'account',
        'sicm_sale'
    ],
    'data': [
        'views/partner_view.xml',
        'report/report_invoice.xml',
        'views/account_move_views.xml',
    ],
    'auto_install': False,
    'application': False,
}