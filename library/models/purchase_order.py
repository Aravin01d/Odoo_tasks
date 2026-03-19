from odoo import models,fields,api

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    product_ids=fields.Many2many("product.product", string="Products",compute="_compute_products", inverse="_compute_partner_products",store=True)
    # product_id = fields.Many2one(domain="[('id','in',product_ids)]")

    # alternate_id=fields.Many2one("product.product", string="Alternate Product")
    # alternate_ids=fields.Many2many("product.product",string="alternate products", compute="_compute_alternate_ids")

    @api.depends('partner_id')
    def _compute_products(self):
        for record in self:
            # print("COMPUTED")
            record.product_ids=record.partner_id.product_ids
            # print(record.product_ids)

    def _compute_partner_products(self):
        for record in self:
            # print("INVERSED")
            record.partner_id.product_ids=record.product_ids


    # @api.depends('partner_id')
    # def _compute_alternate_ids(self):
    #     for rec in self:
    #         print(rec.alternate_ids)
    #         # rec.alternate_ids = False
    #         if rec.product_ids:
    #             # for i in rec.product_ids:
    #                 rec.alternate_ids = rec.product_ids
    #                 # print(rec.alternate_ids.ids)
    #                 print("products:",rec.product_ids)
    #                 print("product_ids:",rec.product_ids.ids)

    # @api.onchange('partner_id')
    # def show_products(self):
    #     for record in self:
    #         record.product_ids=record.partner_id.product_ids
    #         print(self.partner_id.product_ids)
    #     for i in self.product_ids:
    #         print("products",i)


# class PurchaseOrderLine(models.Model):
#     _inherit = 'purchase.order.line'
#
#     product_ids=fields.Many2many("product.product", string="Products",compute="_compute_products", inverse="_compute_partner_products",store=True)
#     product_id = fields.Many2one(domain="[('id','in',product_ids)]")
#
#     # alternate_id=fields.Many2one("product.product", string="Alternate Product")
#     # alternate_ids=fields.Many2many("product.product",string="alternate products", compute="_compute_alternate_ids")
#
#     @api.depends('partner_id')
#     def _compute_products(self):
#         for record in self:
#             print("COMPUTED")
#             record.product_ids=record.partner_id.product_ids
#             print(record.product_ids)
#
#     def _compute_partner_products(self):
#         for record in self:
#             print("INVERSED")
#             record.partner_id.product_ids=record.product_ids
