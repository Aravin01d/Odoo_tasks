import datetime
from datetime import timedelta

from odoo import models,api
from odoo.exceptions import ValidationError

class PurchaseOrder(models.Model):
    """Inherits purchase order model."""
    _inherit = "purchase.order"

    def button_confirm(self):
        """Function to write last reference date in res partner form
        and to check validation."""
        res=super().button_confirm()
        if self.partner_id.last_ref_date and (self.partner_id.last_ref_date <
                datetime.datetime.today()-timedelta(days=90)):
            raise ValidationError("Cannot make this purchase order")
        else:
            self.partner_id.last_ref_date = self.date_approve

        return res

    @api.onchange('partner_id')
    def onchange_partner(self):
        """Function to raise warning if partner has debit."""
        if self.partner_id.debit>0:
            return {
                'warning': {'title': "Warning",
                            'message': "Vendor Has overdue payments",
                            'type': 'notification'
                            },
            }

