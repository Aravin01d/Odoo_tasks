from odoo import models,api

class SaleOrder(models.Model):
    """Inherits sale order model to apply discount on order lines
     by checking customer"""
    _inherit = "sale.order"

    @api.onchange("partner_id")
    def _onchange_partner_id(self):
        """Function to apply discount according to the partner."""
        if self.partner_id.is_vip == True:
            for products in self.order_line:
                products.discount = self.partner_id.vip_discount
        else:
            for products in self.order_line:
                products.discount = 0

    @api.onchange("order_line")
    def _onchange_products(self):
        """Function to apply discount when product is added in  order line."""
        if self.partner_id.is_vip == True:
            for products in self.order_line:
                products.discount = self.partner_id.vip_discount

