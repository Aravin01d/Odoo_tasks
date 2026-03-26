import datetime

from odoo import api,Command,fields,models

class AccountMove(models.Model):
    _inherit = "account.move"
    related_so_ids = fields.Many2many("sale.order",
                                      string="Related Sales Orders",
                                      domain=
                                      "[('invoice_status', '=', 'to invoice'),"
                                      "('partner_id','=',partner_id)]")

    @api.onchange('related_so_ids')
    def onchange_so(self):
        invoice_line = []
        # print(self.related_so_ids.mapped('order_line.product_id'))
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
            print("Invoice line items: ", item)
        self.update({
            "invoice_line_ids":[lines for lines in invoice_line]
        })
        # print("Invoice Lines:",self.invoice_line_ids)
        # for item in invoice_line:
        #         self.update({
        #             "invoice_line_ids":[item]
        #         })
        # else:
        #     self.update({
        #         "invoice_line_ids":[fields.Command.clear()]
        #     })

        # self.update({
        #     # "invoice_date":datetime.date.today(),
        #     "invoice_line_ids": [x for x in invoice_line],
        # })
        # if not self.related_so_ids:
        #     self.update({
        #         "invoice_line_ids": [
        #             (fields.Command.clear())
        #         ]
        #     })
