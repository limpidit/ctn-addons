from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    is_sicm_company = fields.Boolean(compute='_compute_is_sicm_company', store=False)
    sale_order_notes = fields.Text(
        string='Notes commande',
        compute='_compute_sale_order_notes',
        store=True,
        readonly=False,
    )

    @api.depends_context('allowed_company_ids')
    def _compute_is_sicm_company(self):
        for picking in self:
            picking.is_sicm_company = picking.env.company.is_sicm_company()

    @api.depends('sale_id', 'sale_id.order_line', 'sale_id.order_line.display_type', 'sale_id.order_line.name')
    def _compute_sale_order_notes(self):
        for picking in self:
            if picking.sale_id:
                notes = picking.sale_id.order_line.sorted('sequence').filtered(
                    lambda l: l.display_type == 'line_note' and l.name
                )
                picking.sale_order_notes = '\n'.join(notes.mapped('name')) if notes else False
            else:
                picking.sale_order_notes = False


class StockMove(models.Model):
    _inherit = 'stock.move'

    sale_line_description = fields.Text(
        string='Description commande',
        compute='_compute_sale_line_description',
        store=True,
        readonly=False,
    )

    @api.depends('sale_line_id', 'sale_line_id.name')
    def _compute_sale_line_description(self):
        for move in self:
            if move.sale_line_id and move.sale_line_id.name:
                name = move.sale_line_id.name
                product_display_name = move.product_id.display_name or ''
                if name.startswith(product_display_name):
                    extra = name[len(product_display_name):].strip()
                    move.sale_line_description = extra or False
                else:
                    move.sale_line_description = name
            else:
                move.sale_line_description = False
