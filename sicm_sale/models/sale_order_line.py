
from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    increase = fields.Float(string="Increase%", default=0.0)
    net_price = fields.Float(string="Net Price", compute="_compute_net_price", default=0.0, store=True, precompute=True)
    is_sicm_company = fields.Boolean(related="order_id.is_sicm_company",store=False,readonly=True)

    @api.depends('price_unit', 'increase', 'discount')
    def _compute_net_price(self):
        for line in self:
            base = line.price_unit * (1 + (line.increase or 0) / 100)
            line.net_price = base * (1 - (line.discount or 0) / 100)

    # @api.depends('product_uom_qty', 'discount', 'tax_ids', 'net_price', 'increase')
    # def _compute_amount(self):
    #     for line in self:
    #         qty = line.product_uom_qty or 0.0
    #         price_unit = line.net_price

    #         taxes_res = line.tax_ids.compute_all(
    #             price_unit,
    #             currency=line.order_id.currency_id,
    #             quantity=qty,
    #             product=line.product_id,
    #             partner=line.order_id.partner_shipping_id,
    #         )
    #         line.update({
    #             'price_subtotal': taxes_res['total_excluded'],
    #             'price_tax': taxes_res['total_included'] - taxes_res['total_excluded'],
    #             'price_total': taxes_res['total_included'],
    #         })

    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_ids')
    def _compute_amount(self):
        AccountTax = self.env['account.tax']
        for line in self:
            company = line.company_id or self.env.company
            base_line = line._prepare_base_line_for_taxes_computation()
            AccountTax._add_tax_details_in_base_line(base_line, company)
            AccountTax._round_base_lines_tax_details([base_line], company)
            line.price_subtotal = base_line['tax_details']['total_excluded_currency']
            line.price_total = base_line['tax_details']['total_included_currency']
            line.price_tax = line.price_total - line.price_subtotal

    # def _prepare_base_line_for_taxes_computation(self, **kwargs):
    #     self.ensure_one()
    #     base_line = super()._prepare_base_line_for_taxes_computation(**kwargs)
    #     base_line['price_unit'] = self.net_price
    #     base_line['discount'] = 0.0
    #     return base_line

    def _prepare_invoice_line(self, **optional_values):
        self.ensure_one()
        res = super()._prepare_invoice_line(**optional_values)

        if self.order_id.company_id.is_sicm_company():
            res.update({
                'price_unit': self.price_unit,
                'discount': self.discount,
                'increase':  self.increase,
                'net_price': self.net_price,
            })
        return res