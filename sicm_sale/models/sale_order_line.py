
from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    increase = fields.Float(string="Increase%", default=0.0)
    net_price = fields.Float(string="Net Price", compute="_compute_net_price", store=True)

    @api.depends('price_unit', 'increase')
    def _compute_net_price(self):
        for line in self:
            line.net_price = line.price_unit * (1 + line.increase / 100)

    @api.depends('product_uom_qty', 'discount', 'tax_ids', 'net_price', 'increase')
    def _compute_amount(self):
        super()._compute_amount()

    def _prepare_base_line_for_taxes_computation(self, **kwargs):
        self.ensure_one()
        base_line = super()._prepare_base_line_for_taxes_computation(**kwargs)
        base_line['price_unit'] = self.net_price or 0.0
        return base_line