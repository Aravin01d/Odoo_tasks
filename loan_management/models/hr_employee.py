from odoo import fields,models

class ResPartner(models.Model):
    """Inherits employee model."""
    _inherit = "hr.employee"

    loan_not_allowed=fields.Boolean(string="Loan Not Allowed")

