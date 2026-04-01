from odoo import fields, models

class ResPartner(models.Model):
    """Inherits res partner model to add fields."""
    _inherit = "res.partner"

    is_restricted = fields.Boolean(string="Restricted")
    restricted_count = fields.Integer(string="Restricted Count")