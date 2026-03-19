import datetime
from datetime import timedelta
from odoo import models,Command,fields
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit='sale.order'

    def action_confirm(self):
        # print(self.amount_total)
        for rec in self.order_line:
            if rec.price_subtotal<1500:
                self.update({'order_line': [(Command.create({
                    "product_id": self.env.ref('library.delivery_product').id,
                    'price_unit': self.env.ref('library.delivery_product').list_price
                }))]})

        # self.date_order=datetime.datetime.today()-timedelta(days=181)
        # print("Order Date",self.date_order)
        orders=self.env['sale.order'].search([('partner_id','=',self.partner_id),('state','=','draft')])

        print("Orders:",orders)
        order_dates=orders.mapped('date_order')

        print("Order Dates:",order_dates)
        print("Scale Date:",datetime.datetime.today() - timedelta(days=180))

        # for i in order_dates:
        #     if i > datetime.datetime.today() - timedelta(days=180):
        #         raise ValidationError("NOT DATE VALID")

        # for rec in self:
        #     if rec.partner_id.sale_order_count < 2 or rec.amount_total < 10000:
        #         raise ValidationError("NOT VALID")

        return super().action_confirm()

        #     for i in rec.partner_id.sale_order_ids:
        #         l.append(i.date_order)
        #     print(l)
        #     for i in l:
        #         if i > datetime.datetime.today() - timedelta(days=181):
        #             raise ValidationError("NOT VALID")





    # for rec in self:
    #     for i in rec.partner_id.sale_order_ids:
    #         l.append(i.date_order)
    #     print(l)
    #     for i in l:
    #         if i > datetime.datetime.today() - timedelta(days=181):
    #             raise ValidationError("NOT VALID")

    # sale_price=rec.price_unit
    # cost_price=rec.product_template_id.standard_price
    # # print(sale_price)
    # # print(cost_price)
    # cp=cost_price*0.15
    # # print(cp)
    # if sale_price<cp:
    #     raise ValidationError("Cannot confirm order. Some items are sold below allowed margin.")