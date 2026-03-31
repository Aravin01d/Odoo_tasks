from odoo import api, fields, models, tools

class FleetServiceOrderPart(models.Model):
    _name = 'fleet.service.order.part'
    _description = 'Fleet Service Order Part'

    order_id=fields.Many2one("fleet.service.order",string="Order ID")
    product_id=fields.Many2one("product.product",string="Product")
    quantity=fields.Float(string="Quantity")
    unit_price=fields.Float(string="Unit Price")

    @api.onchange("product_id")
    def onchange_part_ids(self):
        print("ok")
        for rec in self:
            rec.unit_price=rec.product_id.list_price
