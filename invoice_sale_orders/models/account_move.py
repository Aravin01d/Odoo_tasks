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
        sale_invoice_ids = []
        if self.related_so_ids:
            for sales in self.related_so_ids:
                    for item in sales.order_line:
                        print("Order line id:",item.id)
                        invoice_line += [(Command.create({
                            "product_id":item.product_id.id,
                            "quantity":item.product_uom_qty,
                            "price_unit":item.price_unit,
                        })
                        )]
                        # for lines in self.invoice_line_ids:
                        #     sale_invoice_ids += [(Command.create({
                        #             "order_line_id":item.id,
                        #             "invoice_line_id":lines.id
                        #     }))]
            # print("Sale Invoice IDS:",sale_invoice_ids)
            for item in invoice_line:
                self.update({
                    "invoice_line_ids": [fields.Command.clear()]
                })
                self.update({
                    "invoice_line_ids":[lines for lines in invoice_line]
                })
            for i in self.invoice_line_ids:
                # print("Invoice Line Ids:",i)
                sale_invoice_ids += [(Command.create({
                    # "order_line_id": item,
                    "invoice_line_id": i.id
                }))]
            print("Sale Invoice IDs:",sale_invoice_ids)

                # self.env['sale.order.line'].update({
                #     "invoice_lines":[line for line in sale_invoice_ids]
                # })
        else:
            self.update({
                "invoice_line_ids":[fields.Command.clear()]
            })

        # for i in self:
        #     print("Invoice line ids:",i.invoice_line_ids)

    def action_post(self):
        """Function to update invoiced quantity in sale order lines"""
        res=super().action_post()
        if self.related_so_ids:
            for ids in self.related_so_ids:
                for items in ids.order_line:
                    print(items.invoice_lines)
                    items.qty_invoiced=items.product_uom_qty

        return res
        # x=self.related_so_ids.order_line
        # for line in x:
        #     line.qty_invoiced=line.product_uom_qty
        # if self.related_so_ids:
        #     for ids in self.related_so_ids:
        #         ids.invoice_status = 'no'

 # ids.invoice_status='no'