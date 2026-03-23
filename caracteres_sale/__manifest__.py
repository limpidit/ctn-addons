{
    'name': 'Caracteres Sale',
    'version': '1.0',
    'description': 'Caracteres Sale',
    'author': 'LimpidIT',
    'license': 'LGPL-3',
    'depends': [
        'caracteres_base',
        'sale',
        'sale_stock',
        'account'
    ],
    'data': [
        'views/sale_order_views.xml',
        'report/ir_actions_report_templates.xml',
    ],
    'auto_install': False,
    'application': False
}
