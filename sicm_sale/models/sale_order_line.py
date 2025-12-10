
from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    increase = fields.Float(string="Increase%", default=0.0)
    net_price = fields.Float(string="Net Price", compute="_compute_net_price", default=0.0, store=True)

    @api.depends('price_unit', 'increase')
    def _compute_net_price(self):
        for line in self:
            line.net_price = line.price_unit * (1 + line.increase / 100)

    @api.depends('product_uom_qty', 'discount', 'tax_ids', 'increase')
    def _compute_amount(self):
        super()._compute_amount()

    def _prepare_base_line_for_taxes_computation(self, **kwargs):
        self.ensure_one()
        base_line = super()._prepare_base_line_for_taxes_computation(**kwargs)
        base_line['price_unit'] = self.net_price or self.price_unit
        return base_line

    def _prepare_invoice_line(self, **optional_values):
        self.ensure_one()
        res = super()._prepare_invoice_line(**optional_values)

        res.update({
            'increase': self.increase,
            'net_price': self.net_price
        })
        return res