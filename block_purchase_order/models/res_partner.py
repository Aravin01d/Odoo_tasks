from odoo import fields, models

class ResPartner(models.Model):
    """Inherits res partner model to add field."""
    _inherit = "res.partner"

    last_ref_date = fields.Datetime("Last Reference Date")
