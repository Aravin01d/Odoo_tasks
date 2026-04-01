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
        self.update({
            "invoice_line_ids": [fields.Command.clear()]
        })
        if self.related_so_ids:
            for sales in self.related_so_ids:
                    for item in sales.order_line:
                        self.update({
                            'invoice_line_ids':[
                                Command.create({
                                    'product_id':item.product_id.id,
                                    'quantity':item.product_uom_qty,
                                    'price_unit':item.price_unit,
                                })
                            ]
                        })

        else:
            self.update({
                "invoice_line_ids":[fields.Command.clear()]
            })

    def action_post(self):
        """Function to link the invoice and related sale orders."""
        res = super().action_post()
        for i in self.invoice_line_ids:
            if self.related_so_ids:
                for sales in self.related_so_ids:
                    for item in sales.order_line:
                        item.invoice_lines=i
        if self.related_so_ids:
            for ids in self.related_so_ids:
                for items in ids.order_line:
                    items.qty_invoiced = items.product_uom_qty

        return res