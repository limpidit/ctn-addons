
from odoo import models, api, fields


class AccountMove(models.Model):
    _inherit = "account.move"

    is_sicm_company = fields.Boolean(compute="_compute_is_sicm_company",store=False)

    @api.depends('company_id')
    def _compute_is_sicm_company(self):
        for order in self:
            order.is_sicm_company = bool(order.company_id) and order.company_id.is_sicm_company()

    def _prepare_product_base_line_for_taxes_computation(self, product_line):
        self.ensure_one()
        base_line = super()._prepare_product_base_line_for_taxes_computation(product_line)

        if self.is_invoice(include_receipts=True):
            base_line['price_unit'] = product_line.net_price or product_line.price_unit

        return base_line