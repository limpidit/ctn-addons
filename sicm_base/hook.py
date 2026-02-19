
from odoo.api import Environment, SUPERUSER_ID


def post_init_hook(env):

    Company = env['res.company'].sudo()
    IMD = env['ir.model.data'].sudo()

    company = Company.search([('vat', '=', 'FR19303914550')], limit=1)
    if not company:
        return

    imd = IMD.search([('module', '=', 'sicm_base'), ('name', '=', 'company_sicm')], limit=1)
    if imd:
        if imd.model != 'res.company' or imd.res_id != company.id:
            imd.write({'model': 'res.company', 'res_id': company.id, 'noupdate': True})
        return

    IMD.create({
        'module': 'sicm_base',
        'name': 'company_sicm',
        'model': 'res.company',
        'res_id': company.id,
        'noupdate': True,
    })