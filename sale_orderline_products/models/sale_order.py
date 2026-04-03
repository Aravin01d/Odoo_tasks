from odoo import  Command, fields, models
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    """Inherits sale order model to add fields, buttons and edit sale order line."""
    _inherit = "sale.order"

    product_variant_ids = fields.Many2many(
        "product.product", "product_sale_order_variant_rel",
        'product_variant_id','sale_order_id',
        string="Products",
    )
    variant_quantity = fields.Float(string="Quantity")

    def action_add_products(self):
        """Function to add selected products to order line."""
        products = self.order_line.mapped('product_id')
        if self.variant_quantity==0:
                raise ValidationError("Quantity can't be zero")

        for product in self.product_variant_ids:
            for items in self.order_line:
                if product == items.product_id:
                    items.product_uom_qty+= self.variant_quantity
                    break
            if product not in products:
                self.write({
                    'order_line':[
                        Command.create({
                            'product_id':product.id,
                            'product_uom_qty':self.variant_quantity
                        })
                    ]
                })
        self.write({
            'product_variant_ids': [(fields.Command.clear())],
            'variant_quantity': 0
        })