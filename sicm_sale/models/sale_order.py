
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    partner_internal_note = fields.Html(string="Customer notes", related="partner_id.comment", readonly=True)
    is_sicm_company = fields.Boolean(compute="_compute_is_sicm_company",store=False)

    @api.depends('company_id')
    def _compute_is_sicm_company(self):
        for order in self:
            order.is_sicm_company = bool(order.company_id) and order.company_id.is_sicm_company()

    @api.constrains('client_order_ref', 'partner_id', 'company_id')
    def _check_client_order_ref_required(self):
        for order in self:
            if (order.company_id and order.company_id.is_sicm_company() and order.partner_id.order_reference_required and not order.client_order_ref):
                raise ValidationError(_("You must set a Customer Reference."))

    def copy(self, default=None):
        self.ensure_one()
        default = dict(default or {})

        if (self.company_id and self.company_id.is_sicm_company() and self.partner_id.order_reference_required):
            default.setdefault("client_order_ref", self.client_order_ref or "")

        return super().copy(default)
