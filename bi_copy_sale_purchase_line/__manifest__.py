# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Copy Sale and Purchase Order Line',
    'version': '19.0.0.0',
    'category': 'Sales',
    'license': 'OPL-1',
    'summary': 'Copy sale order line copy purchase order line duplicate sale order line duplicate purchase order line Copy sale line copy purchase line duplicate sale line duplicate purchase line Copy sales order line duplicate sales order line copy sales line',
    'description': """
        
            Copy Sale Purchase Line in Odoo,
            Copy sale order line in odoo,
            Copy purchase order line in odoo,
            Copy button in sale purchase line in odoo,
            Easy to copy sale and purchase order line in odoo,

    """,
    'author': 'BROWSEINFO',
    'website': 'https://www.browseinfo.com/demo-request?app=bi_copy_sale_purchase_line&version=19&edition=Community',
    'depends': ['base', 'sale_management', 'purchase_stock'],
    'data': [
        'views/sale_purchase_view.xml'
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'live_test_url': 'https://www.browseinfo.com/demo-request?app=bi_copy_sale_purchase_line&version=19&edition=Community',
    "images": ['static/description/Banner.gif'],
}
