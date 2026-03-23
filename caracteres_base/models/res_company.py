from odoo import models, fields


class ResCompany(models.Model):
    _inherit = "res.company"

    is_caracteres = fields.Boolean(string="Caracteres", default=False)

    def is_caracteres_company(self):
        self.ensure_one()
        caracteres = self.env.ref("caracteres_base.company_caracteres", raise_if_not_found=False)
        if caracteres:
            return self == caracteres

        return bool(self.vat and self.vat == "FR31403497761")
