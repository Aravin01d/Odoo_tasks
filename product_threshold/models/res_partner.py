from odoo import fields, models

class ResPartner(models.Model):
    """Inherits res_partner model."""
    _inherit = "res.partner"

    product_variant_ids = fields.Many2many('product.product',
                                         'product_variant_rel',
                                         'product_variant_id',
                                         'res_partner_id',string="Products")

    def action_recalculate(self):
        """Function to fetch product threshold value and add products to partner."""
        product_threshold = float(self.env['ir.config_parameter'].sudo().get_param('product_threshold.products_threshold'))
        orders = self.env['sale.order'].search([("partner_id",'=',self.id)])
        order_lines = self.env['sale.order.line'].search([
            ('order_partner_id','=',self.id)])
        dict = {}
        for i in order_lines:
            qts = i.product_uom_qty
            products = i.product_id.id
            if products in dict:
                dict[products] += qts
            else:
                dict[products] = qts
        top_products = [k for k in dict if dict[k]>=product_threshold]
        for i in top_products:
            self.update({
                'product_variant_ids':[(fields.Command.link(i))]
            })

    def action_add_so(self):
        """Function to create sale order with products in products field."""
        products_list = []
        for i in self.product_variant_ids:
            products_list += [(fields.Command.create({
                "product_id": i.id
            }))]
        order_data = {
            'partner_id': self.id,
            'order_line':[x for x in products_list]
        }
        new_sale_order = self.env['sale.order'].create(order_data)