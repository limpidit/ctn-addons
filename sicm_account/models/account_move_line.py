
from odoo import models, fields, api


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    increase = fields.Float(string="Increase%", default=0.0)
    net_price = fields.Float(string="Net Price", default=0.0, compute="_compute_net_price", store=True)

    @api.depends('price_unit', 'increase', 'discount')
    def _compute_net_price(self):
        for line in self:
            if line.move_id.company_id.is_sicm_company():
                for line in self:
                    base = line.price_unit * (1 + (line.increase or 0) / 100)
                    line.net_price = base * (1 - (line.discount or 0) / 100)

    @api.depends(
        'quantity',
        'net_price',
        'discount',
        'price_unit',
        'tax_ids',
        'currency_id',
        'move_id.move_type',
        'move_id.partner_id',
    )
    def _compute_totals(self):
        if self.move_id.company_id.is_sicm_company():
            for line in self:
                qty = line.quantity or 0.0
                price_unit = line.net_price
                currency = line.currency_id or line.move_id.currency_id
                partner = line.partner_id or line.move_id.partner_id

                taxes_res = line.tax_ids.compute_all(
                    price_unit,
                    currency=currency,
                    quantity=qty,
                    product=line.product_id,
                    partner=partner,
                )

                line.price_subtotal = taxes_res['total_excluded']
                line.price_total = taxes_res['total_included']

        else:
            super(AccountMoveLine, self)._compute_totals()