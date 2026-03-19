from odoo import  Command, fields, models

class SaleOrder(models.Model):
    _inherit = "sale.order"

    product_ids=fields.Many2many(
        "product.product",
        string="Products",
    )
    quantity=fields.Float(string="Quantity")

    def action_add_products(self):
        products=self.order_line.mapped('product_id')

        for product in self.product_ids:
            for items in self.order_line:
                if product == items.product_id:
                    items.product_uom_qty+= self.quantity
                    break
            if product not in products:
                self.write({
                    'order_line':[
                        Command.create({
                            'product_id':product.id,
                            'product_uom_qty':self.quantity
                        })
                    ]
                })
