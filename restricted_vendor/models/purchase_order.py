from odoo import fields, models, api
from odoo.exceptions import ValidationError

class PurchaseOrder(models.Model):
    """Inherits purchase order model to add fields.."""
    _inherit = "purchase.order"

    is_restricted = fields.Boolean(related="partner_id.is_restricted",
                                   string="Is Restricted")
    restricted_count = fields.Integer(related="partner_id.restricted_count",
                                      string="Restricted Count")

    @api.onchange("partner_id","order_line")
    def onchange_partner_id(self):
        """Function to raise validation error on basis of restricted fields."""
        l  =[]
        for rec in self.order_line.filtered(
                lambda x: x.display_type not in ('line_note','line_section')):
            l += rec
        print(l)
        if (self.is_restricted == True and len(l)>self.restricted_count
                and self.order_line):
            raise ValidationError("Order lines restricted")

    def button_confirm(self):
        """Function to call onchange_partner_id() on confirm button click."""
        res = super().button_confirm()
        self.onchange_partner_id()
        return res