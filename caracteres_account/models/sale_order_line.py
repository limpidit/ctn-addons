from odoo import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _prepare_invoice_line(self, **optional_values):
        self.ensure_one()
        res = super()._prepare_invoice_line(**optional_values)

        if self.order_id.company_id.is_caracteres_company():
            res.update({
                'line_reference': self.line_reference,
                'width': self.width,
                'height': self.height,
                'copies': self.copies,
                'num_models': self.num_models,
            })
        return res
