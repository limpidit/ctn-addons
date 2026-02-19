
from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    order_reference_required = fields.Boolean(string="Order Reference Required")
    show_order_reference_required = fields.Boolean(compute="_compute_show_order_reference_required",store=False)

    @api.depends_context('allowed_company_ids')
    def _compute_show_order_reference_required(self):
        is_sicm_company = self.env.company.is_sicm_company()
        for rec in self:
            rec.show_order_reference_required = is_sicm_company