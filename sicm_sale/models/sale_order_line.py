
from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    increase = fields.Float(string="Increase%", default=0.0)
    net_price = fields.Float(string="Net Price", compute="_compute_net_price", store=True)

    @api.depends('price_unit', 'increase')
    def _compute_net_price(self):
        for line in self:
            line.net_price = line.price_unit * (1 + line.increase / 100)