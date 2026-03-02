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

    def action_read_and_log_file(self):
        self.ensure_one()
        
        if not self.csv_file:
            raise UserError(_("Veuillez charger un fichier CSV."))

        try:
            raw_file = base64.b64decode(self.csv_file)
            decoded_file = None
            
            for enc in ['utf-8', 'cp1252', 'iso-8859-15', 'mac_roman']:
                try:
                    decoded_file = raw_file.decode(enc)
                    break
                except UnicodeDecodeError:
                    continue
            
            if decoded_file is None:
                decoded_file = raw_file.decode('utf-8', errors='replace')
            
            file_stream = StringIO(decoded_file)
            csv_reader = csv.reader(file_stream, delimiter=';') 
            
            _logger.info("=== DÉBUT DE LA LECTURE DU FICHIER CSV ===")
            
            headers = next(csv_reader, None)
            _logger.info("En-têtes du CSV : %s", headers)

            for row_index, row in enumerate(csv_reader, start=2):
                clean_row = [str(val).strip() for val in row]
                _logger.info("Ligne %s : %s", row_index, clean_row)

            _logger.info("=== FIN DE LA LECTURE DU FICHIER CSV ===")

        except Exception as e:
            raise UserError(_("Erreur lors de la lecture du fichier : %s") % str(e))

        return {'type': 'ir.actions.act_window_close'}