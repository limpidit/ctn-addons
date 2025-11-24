
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    order_reference_required = fields.Boolean(related="partner_id.order_reference_required",string="Order Reference Required",readonly=True,store=False)
