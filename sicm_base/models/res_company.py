
from odoo import models, fields


class ResCompany(models.Model):
    _inherit = "res.company"

    is_sicm = fields.Boolean(string="SICM", default=False)

    def is_sicm_company(self):
        self.ensure_one()
        sicm = self.env.ref("sicm_base.company_sicm", raise_if_not_found=False)
        if sicm:
            return self == sicm

        return bool(self.vat and self.vat == "FR19303914550")
