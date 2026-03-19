from odoo import fields, models, api
from odoo.addons.test_convert.tests.test_env import record

class AccountMove(models.Model):
    _inherit = 'account.move'

    checkout_id=fields.Many2one("checkouts.model",string="Checkout ID")
    product_ids=fields.Many2many("product.product", string="Products")

    # def get_checkout_id(self):

    def action_invoice_sent(self):
        print(self.checkout_id)
        return super().action_invoice_sent()

    @api.depends('partner_id')
    def show_products(self):
        for record in self:
            record.product_ids=record.partner_id.product_ids
            print(self.partner_id.product_ids)
        for i in self.product_ids:
            print("products",i)


    # def compute_products(self):
    #     products=self.env['res.partner'].


    # def
    # def get_checkout_id(self):

