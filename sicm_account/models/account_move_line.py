
from odoo import models, fields, api


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    increase = fields.Float(string="Increase%", default=0.0)
    net_price = fields.Float(string="Net Price", compute="_compute_net_price", store=True)

    @api.depends('price_unit', 'increase')
    def _compute_net_price(self):
        for line in self:
            line.net_price = line.price_unit * (1 + line.increase / 100)

    @api.depends('quantity', 'discount', 'tax_ids', 'increase', 'currency_id')
    def _compute_totals(self):
        super()._compute_totals()