from odoo import models, fields

class SettingsModel(models.TransientModel):
    """Inherits settings model."""
    _inherit= 'res.config.settings'

    products_threshold=fields.Float(string="Product Threshold", help="Set the product threshold for customer", config_parameter="product_threshold.products_threshold")