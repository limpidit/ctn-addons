{
    'name': 'SICM Sale',
    'version': '1.0',
    'description': 'SICM Sale',
    'author': 'Limpid IT',
    'license': 'LGPL-3',
    'depends': [
        'sale',
        'sale_stock',
        'account'
    ],
    'data': [
        'views/res_partner_views.xml',
        'views/sale_order_views.xml',
        'report/ir_actions_report_templates.xml'
    ],
    'auto_install': False,
    'application': False
}