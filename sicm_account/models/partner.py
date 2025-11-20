
from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    insured_amount = fields.Monetary(
        string='Insured Amount',
        groups='account.group_account_invoice,account.group_account_readonly'
    )

    