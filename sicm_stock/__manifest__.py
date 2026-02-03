{
    'name': 'SICM Stock',
    'version': '1.0',
    'description': 'SICM Stock',
    'author': 'LimpidIT',
    'license': 'LGPL-3',
    'depends': [
        'stock',
        'sicm_base',
        'delivery'
    ],
    'data': [
        'views/delivery_carrier_views.xml',
        'report/report_stockpicking_operations.xml',
    ],
    'auto_install': False,
    'application': False,
    'assets': {
        
    }
}