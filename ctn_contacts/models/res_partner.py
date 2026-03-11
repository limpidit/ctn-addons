
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    customer_ref = fields.Char(string="Customer ref")

    @api.constrains('category_id', 'is_company')
    def _check_category_required_for_group(self):
        for partner in self:
            if partner.is_company and not partner.category_id:
                raise ValidationError(_("You must set at least one tag on the contact."))