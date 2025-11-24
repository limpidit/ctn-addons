
from odoo import models, fields


class ResPartner(models.Model):
    _inherit = "res.partner"

    order_reference_required = fields.Boolean(string="Order Reference Required")