from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = "account.move"

    is_caracteres_company = fields.Boolean(compute="_compute_is_caracteres_company", store=False)

    @api.depends('company_id')
    def _compute_is_caracteres_company(self):
        for move in self:
            move.is_caracteres_company = bool(move.company_id) and move.company_id.is_caracteres_company()
