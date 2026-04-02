from docutils.parsers import null

from odoo import fields, models, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    most_sold_product_id = fields.Many2one("product.product",string="Most Sold Product", compute="_compute_most_sold_product_id")
    total_sold_quantity = fields.Float(string="Total Sold Quantity")
    minimum_sale_price = fields.Float(string="Minimum Sold Price")
    maximum_sale_price = fields.Float(string="Maximum Sold Price")

    def _compute_most_sold_product_id(self):
        if self.sale_order_ids:
            lines = self.sale_order_ids.order_line
            # print("Order Lines:",lines)
            prods = {}
            for l in lines:
                    product = l.product_id
                    qts = l.product_uom_qty
                    if product in prods:
                        prods[product] += qts
                    else:
                        prods[product] = qts
            print("Products and qts:",prods)
            l=[]
            for k in lines:
                # print(k.product_uom_qty)
                l += k.product_id
                # qts += k.product_uom_qty
            self.most_sold_product_id = max(set(l), key=l.count)
            # self.total_sold_quantity = max(set(qts), key=qts.count)
            # self.total_sold_quantity = self.most_sold_product_id.sales_count
        else:
            self.most_sold_product_id = null

    # @api.onchange("most_sold_product_id")
    # def onchange_most_sold_product(self):
    #     self.total_sold_quantity = self.most_sold_product_id.sales_count

        # prices = self.most_sold_product_id.sale_order_ids.order_line.mapped('price_unit')
        # print("prices:", prices)
        # self.minimum_sale_price = 2.0
        # self.maximum_sale_price = 31.0

# , compute="_compute_most_sold_product_id"