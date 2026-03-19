from odoo import api,fields,models

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    product_ids=fields.Many2many("product.product", string="Products",compute="_compute_products", inverse="_compute_partner_products",store=True)
    # product_line_id = fields.Many2one("product.product",domain="[('id','in',product_ids)]")
    product_id=fields.Many2one(domain="[('id','in',product_ids)]")

    # alternate_id=fields.Many2one("product.product", string="Alternate Product")
    # alternate_ids=fields.Many2many("product.product",string="alternate products", compute="_compute_alternate_ids")

    @api.depends('partner_id')
    def _compute_products(self):
        for record in self:
            print("COMPUTED")
            record.product_ids=record.partner_id.product_ids
            print(record.product_ids)
            # print(record.product_line_id)

    def _compute_partner_products(self):
        for record in self:
            print("INVERSED")
            record.partner_id.product_ids=record.product_ids