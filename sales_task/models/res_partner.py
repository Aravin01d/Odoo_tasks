from odoo import api,fields,models

class ResPartner(models.Model):
    _inherit = 'res.partner'
    most_sold_product_id = fields.Many2one("product.product",string="Most Sold Product", compute="_compute_most_sold_product_id")
    total_sold_quantity = fields.Float(string="Total Sold Quantity")
    minimum_sale_price = fields.Float(string="Minimum Sold Price")
    maximum_sale_price = fields.Float(string="Maximum Sold Price")
    cos = fields.Integer(string="sale count of msp product", compute="_compute_cos")

    @api.depends('most_sold_product_id')
    def _compute_cos(self):
        for record in self:
            lines = self.sale_order_ids.order_line
            prd_id = lines.filtered(
                lambda l: l.product_id == record.most_sold_product_id)
            print("Prd Id:", prd_id)
            line_sale_id = prd_id.mapped('order_id.id')
            record.cos = len(line_sale_id)

    def action_view_top_sales(self):
        for record in self:
            lines = self.sale_order_ids.order_line
            prd_id = lines.filtered(lambda l: l.product_id == record.most_sold_product_id)
            print("Prd Id:",prd_id)
            line_sale_id = prd_id.mapped('order_id.id')
            print(line_sale_id)
            return {
                'type': 'ir.actions.act_window',
                'name':'Sale Orders',
                'res_model': 'sale.order',
                'view_mode': 'list',
                'domain':[('id','=',line_sale_id)],
                'context':"{'create':False}",
            }

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
            # print("Products and qts:",prods)
            max_qty = 0
            most_sold_product_id = None
            for product,qts in prods.items():
                # print(product,qts)
                if qts > max_qty:
                    max_qty = qts
                    most_sold_product_id = product
            self.most_sold_product_id = most_sold_product_id
            self.total_sold_quantity = max_qty
            # print("Most Sold Product:",self.most_sold_product_id)

            product_lines = lines.filtered(lambda l: l.product_id == most_sold_product_id)
            prices = product_lines.mapped("price_unit")
            self.maximum_sale_price = max(prices)
            self.minimum_sale_price = min(prices)

        else:
            self.most_sold_product_id = None

    # @api.depends('most_sold_product_id')
    # def _compute_count(self):
    #     for rec in self:
    #         rec.sale_orders_count = rec.most_sold_product_id.sales_count
    #         print(rec.sale_orders_count)

    # @api.depends('most_sold_product_id')
    # def _compute_sale_order_count(self):
    #     print("HERE hr")
    #     for rec in self:
    #         rec.sale_order_count = rec.most_sold_product_id.sales_count
    #         print(rec.sale_order_count)
        # print(self.sale_order_count)
    #
