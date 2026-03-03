import base64
import csv
import logging
from io import StringIO
from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class ImportProductAttributeWizard(models.TransientModel):
    _name = 'import.product.attribute.wizard'
    _description = "Wizard d'import CSV pour les attributs"

    csv_file = fields.Binary(string="Fichier CSV", required=True)
    file_name = fields.Char(string="Nom du fichier")

    def action_import_file(self):
        self.ensure_one()
        
        if not self.csv_file:
            raise UserError(_("Veuillez charger un fichier CSV."))

        try:
            raw_file = base64.b64decode(self.csv_file)
            decoded_file = None
            
            for enc in ['utf-8-sig', 'utf-8', 'utf-16', 'cp1252', 'iso-8859-15', 'mac_roman']:
                try:
                    test_decode = raw_file.decode(enc)
                    if '\x00' in test_decode and enc not in ['utf-16']:
                        continue
                    decoded_file = test_decode
                    break
                except UnicodeDecodeError:
                    continue
            
            if decoded_file is None:
                decoded_file = raw_file.decode('utf-8', errors='replace')
            
            decoded_file = decoded_file.replace('\x00', '')
            
            file_stream = StringIO(decoded_file, newline='')
            csv_reader = csv.reader(file_stream, delimiter=';') 
            
            _logger.info("=== DÉBUT DE L'IMPORT DES ATTRIBUTS ===")
            
            headers = next(csv_reader, None)
            current_product = None

            for row_index, row in enumerate(csv_reader, start=2):
                clean_row = [str(val).strip() for val in row]
                
                if len(clean_row) < 4:
                    continue

                ref_interne = clean_row[1]
                attr_name = clean_row[2]
                val_ids_str = clean_row[3]

                if ref_interne:
                    current_product = self.env['product.template'].search([('default_code', '=', ref_interne)], limit=1)
                    if not current_product:
                        _logger.warning("Ligne %s : Produit ignoré. Référence '%s' introuvable en base.", row_index, ref_interne)
                        continue

                if not current_product:
                    _logger.warning("Ligne %s : Ligne ignorée. Aucun produit défini.", row_index)
                    continue

                if not attr_name:
                    continue

                attribute = self.env['product.attribute'].search([('name', '=', attr_name)], limit=1)
                if not attribute:
                    _logger.warning("Ligne %s : Attribut '%s' introuvable en base pour le produit [%s].", row_index, attr_name, current_product.default_code)
                    continue

                val_ids_str_clean = val_ids_str.replace('.', ',')
                val_ids = [int(v.strip()) for v in val_ids_str_clean.split(',') if v.strip().isdigit()]

                if not val_ids:
                    _logger.warning("Ligne %s : Aucune valeur valide trouvée pour l'attribut '%s'.", row_index, attr_name)
                    continue

                existing_line = current_product.attribute_line_ids.filtered(lambda l: l.attribute_id.id == attribute.id)

                if existing_line:
                    existing_line.write({
                        'value_ids': [(4, v_id) for v_id in val_ids]
                    })
                    _logger.info("Ligne %s : Valeurs ajoutées à l'attribut '%s' sur le produit [%s].", row_index, attr_name, current_product.default_code)
                else:
                    self.env['product.template.attribute.line'].create({
                        'product_tmpl_id': current_product.id,
                        'attribute_id': attribute.id,
                        'value_ids': [(6, 0, val_ids)]
                    })
                    _logger.info("Ligne %s : Nouvel attribut '%s' créé sur le produit [%s].", row_index, attr_name, current_product.default_code)

            _logger.info("=== FIN DE L'IMPORT DES ATTRIBUTS ===")

        except Exception as e:
            raise UserError(_("Erreur lors de la lecture du fichier : %s") % str(e))

        return {'type': 'ir.actions.act_window_close'}