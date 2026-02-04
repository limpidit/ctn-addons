
from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    vendor_label = fields.Char( string="Vendor Ref", compute="_compute_vendor_label")

    @api.depends('product_id', 'picking_id.partner_id', 'product_uom_qty', 'product_uom', 'date')
    def _compute_vendor_label(self):
        for move in self:
            label = False
            partner = move.picking_id.partner_id
            product = move.product_id
            if partner and product:
                seller = product._select_seller(partner_id=partner, quantity=move.product_uom_qty or 1.0, date=move.date or fields.Date.context_today(move), uom_id=move.product_uom)
                if seller:
                    code = (seller.product_code or "").strip()
                    if code:
                        label = f"{code}"
            move.vendor_label = label
