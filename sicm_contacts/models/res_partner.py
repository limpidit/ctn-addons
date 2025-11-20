
from odoo import models, fields

class ResPartner(models.Model):
    _inherit = "res.partner"

    category_id = fields.Many2many(
        required=True
    )
