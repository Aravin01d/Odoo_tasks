import datetime

from odoo import api,Command,fields,models

class AccountMove(models.Model):
    """Inherits Account Move Model."""
    _inherit = "account.move"
    related_so_ids = fields.Many2many("sale.order",
                                      string="Related Sales Orders",
                                      domain=
                                      "[('invoice_status', '=', 'to invoice'),"
                                      "('partner_id','=',partner_id)]")

    @api.onchange('related_so_ids')
    def onchange_so(self):
        """Function to update invoice lines."""
        invoice_line = []
        if self.related_so_ids:
            for sales in self.related_so_ids:
                    for item in sales.order_line:
                        invoice_line += [(Command.create({
                            "product_id":item.product_id.id,
                            "quantity":item.product_uom_qty,
                            "price_unit":item.price_unit,
                        })
                        )]
            for item in invoice_line:
                self.update({
                    "invoice_line_ids": [fields.Command.clear()]
                })
                self.update({
                    "invoice_line_ids":[lines for lines in invoice_line]
                })
        else:
            self.update({
                "invoice_line_ids":[fields.Command.clear()]
            })

    def action_post(self):
        """Function to update invoiced quantity in sale order lines"""
        res=super().action_post()
        # if self.related_so_ids:
        # for ids in self.related_so_ids:
        #     for items in ids.order_line:
        #         print(items.invoice_lines)
        #         items.qty_invoiced=items.product_uom_qty

        return res
        # x=self.related_so_ids.order_line
        # for line in x:
        #     line.qty_invoiced=line.product_uom_qty
        # if self.related_so_ids:
        #     for ids in self.related_so_ids:
        #         ids.invoice_status = 'no'


 # ids.invoice_status='no'