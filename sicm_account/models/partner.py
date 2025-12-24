
from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    insured_amount = fields.Monetary(string='Insured Amount',groups='account.group_account_invoice,account.group_account_readonly')
    is_sicm_company = fields.Boolean(compute="_compute_is_sicm_company", store=False)

    @api.depends_context("allowed_company_ids")
    def _compute_is_sicm_company(self):
        is_sicm = self.env.company.is_sicm_company()
        for partner in self:
            partner.is_sicm_company = is_sicm

    