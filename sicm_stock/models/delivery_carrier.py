
from odoo import models, fields, _
from odoo.exceptions import UserError


class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'

    warehouse_ids = fields.Many2many('stock.warehouse', string='Warehouses')

    def _match(self, partner, source):
        self.ensure_one()
        return super()._match(partner, source) and self._match_warehouse(source)

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