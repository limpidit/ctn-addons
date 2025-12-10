
from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def _prepare_product_base_line_for_taxes_computation(self, product_line):
        self.ensure_one()
        base_line = super()._prepare_product_base_line_for_taxes_computation(product_line)

        if self.is_invoice(include_receipts=True):
            base_line['price_unit'] = product_line.net_price or product_line.price_unit

        return base_line