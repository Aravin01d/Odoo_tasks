from odoo import fields,  models, _

class ProductMenu(models.TransientModel):
    _name = 'product.menu'
    _description = 'Product Menu'
    # product_ids=fields.Many2many(
    #     'product.product',string='Products',
    # )
    product_ids = fields.Many2many("product.product", string="Product")
    # lst_price = fields.Float(related="product_ids")
    fixed_price= fields.Float(string='Fixed Price')
    percentage_price=fields.Float(string='Percentage Price')

    def view_product_wizard(self):
        return {
            'name': _('Product Menu'),
            'type': 'ir.actions.act_window',
            'res_model': 'product.menu',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
        }

    def action_update_fixed(self):
        for record in self:
            print(record.fixed_price)

            # sale_price=record.product_ids.lst_price
            for i in record.product_ids:
                i.lst_price = record.fixed_price

            # print(record.product_ids.lst_price)

    def action_update_percentage(self):
        for record in self:
            print(record.percentage_price)

            for i in record.product_ids:

            # plp=record.product_ids.lst_price

                i.lst_price = i.lst_price + (i.lst_price*(record.percentage_price))

            # print(record.product_ids.lst_price)