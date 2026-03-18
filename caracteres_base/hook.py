from odoo.api import Environment, SUPERUSER_ID


def post_init_hook(env):

    Company = env['res.company'].sudo()
    IMD = env['ir.model.data'].sudo()

    company = Company.search([('vat', '=', 'FR31403497761')], limit=1)
    if not company:
        return

    imd = IMD.search([('module', '=', 'caracteres_base'), ('name', '=', 'company_caracteres')], limit=1)
    if imd:
        if imd.model != 'res.company' or imd.res_id != company.id:
            imd.write({'model': 'res.company', 'res_id': company.id, 'noupdate': True})
        return

    IMD.create({
        'module': 'caracteres_base',
        'name': 'company_caracteres',
        'model': 'res.company',
        'res_id': company.id,
        'noupdate': True,
    })
