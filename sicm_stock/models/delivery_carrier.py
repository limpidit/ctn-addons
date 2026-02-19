
from odoo import models, fields, _, api
from odoo.exceptions import UserError


class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'

    warehouse_ids = fields.Many2many('stock.warehouse', string='Warehouses')
    is_sicm_company = fields.Boolean(compute="_compute_is_sicm_company",store=False)

    @api.depends_context("allowed_company_ids")
    def _compute_is_sicm_company(self):
        for carrier in self:
            carrier.is_sicm_company = carrier.env.company.is_sicm_company()

    def _match(self, partner, source):
        self.ensure_one()
        res = super()._match(partner, source)

        company = getattr(source, "company_id", False)
        if company and company.is_sicm_company():
            res = res and self._match_warehouse(source)

        return res

    def _match_warehouse(self, source):
        self.ensure_one()
        if not self.warehouse_ids:
            return True

        if source._name == 'sale.order':
            warehouse = source.warehouse_id
        elif source._name == 'stock.picking':

            warehouse = source.picking_type_id.warehouse_id
        else:
            raise UserError(_("Invalid source document type"))

        return bool(warehouse) and warehouse in self.warehouse_ids