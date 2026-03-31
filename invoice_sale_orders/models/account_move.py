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
        self.update({
            "invoice_line_ids": [fields.Command.clear()]
        })
        invoice_line = []
        sale_invoice_ids = []
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
            # for i in self.invoice_line_ids:
            #     print("Line ids:",i.ids)
            #     print("Line ID:",i.id)
            #     print("Line:",i)
                            # item.invoice_lines=i.id
                # print("Sale orderline invoice_lines: ",item.invoice_lines)
                # print("Invoice line IDs:",i.id)

        else:
            self.update({
                "invoice_line_ids":[fields.Command.clear()]
            })


        # for i in self:
        #     print("Invoice line ids:",i.invoice_line_ids)

    def action_post(self):
        """Function to update invoiced quantity in sale order lines"""
        res=super().action_post()
        for i in self.invoice_line_ids:
            if self.related_so_ids:
                for sales in self.related_so_ids:
                    for item in sales.order_line:
                        item.invoice_lines=i
            # print("Line ids:", i.ids)
            # print("Line ID:", i.id)
            # print("Line:", i)
        if self.related_so_ids:
            for ids in self.related_so_ids:
                for items in ids.order_line:
                    items.qty_invoiced=items.product_uom_qty

        return res
        # x=self.related_so_ids.order_line
        # for line in x:
        #     line.qty_invoiced=line.product_uom_qty
        # if self.related_so_ids:
        #     for ids in self.related_so_ids:
        #         ids.invoice_status = 'no'

 # ids.invoice_status='no'


# print("Order line id:",item.id)
# invoice_line += [(Command.create({
#     "product_id":item.product_id.id,
#     "quantity":item.product_uom_qty,
#     "price_unit":item.price_unit,
# })
# )]
# sale_invoice_ids += [(Command.create({
#     "invoice_line_id":
# }))]
# for item in invoice_line:
#     self.update({
#         "invoice_line_ids": [fields.Command.clear()]
#     })
#     self.update({
#         "invoice_line_ids":[lines for lines in invoice_line]
#     })

# self.env['sale.order.line'].update({
#     "invoice_lines":[line for line in sale_invoice_ids]
# })