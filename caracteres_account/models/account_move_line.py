from odoo import models, fields, api


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    is_caracteres_company = fields.Boolean(
        related="move_id.is_caracteres_company",
        store=False,
        readonly=True
    )

    line_reference = fields.Char(string="Reference")
    width = fields.Float(string="Width", digits=(16, 3))
    height = fields.Float(string="Height", digits=(16, 3))
    copies = fields.Integer(string="Copies", default=1)
    num_models = fields.Integer(string="Models", default=1)

    area = fields.Float(
        string="Quantity",
        compute="_compute_area",
        store=True,
        digits=(16, 2)
    )

    total_surface = fields.Float(
        string="Total Surface",
        related='quantity',
        readonly=False
    )

    @api.depends('width', 'height')
    def _compute_area(self):
        for line in self:
            line.area = (line.width or 0.0) * (line.height or 0.0)

    @api.onchange('width', 'height', 'copies', 'num_models')
    def _onchange_dimensions(self):
        for line in self:
            w = line.width or 0.0
            h = line.height or 0.0
            c = line.copies or 0
            m = line.num_models or 0
            line.quantity = w * h * c * m
