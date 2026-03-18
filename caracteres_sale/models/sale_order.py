from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    is_caracteres_company = fields.Boolean(compute="_compute_is_caracteres_company", store=False)

    @api.depends('company_id')
    def _compute_is_caracteres_company(self):
        for order in self:
            order.is_caracteres_company = bool(order.company_id) and order.company_id.is_caracteres_company()
