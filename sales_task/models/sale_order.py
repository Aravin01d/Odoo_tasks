from email.policy import default

from odoo import fields, models, api

from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = "sale.order"

    delivery_remark = fields.Text(string="Delivery Remark")
    is_urgent_delivery = fields.Boolean(string="Is Urgent Delivery")
    preferred_delivery_time = fields.Selection([
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon'),
        ('evening', 'Evening'),
    ],
    string="Preferred Delivery Time")
    discount_approved = fields.Boolean(string="Discount Approved")
    discount_approved_by = fields.Many2one("res.users",string="Discount Approved By")

    # default = lambda self: self.env.user,
    def action_approve_discount(self):
        for rec in self:
            print(rec.order_line.mapped('discount'))
            disc = rec.order_line.mapped('discount')
            for i in disc:
                if i > 0 :
                    pass
                else:
                    raise ValidationError("Atleast one discount need be there")

            # print(rec.discount)
        # print(lines)
        # print("ok")

    @api.onchange("discount_approved")
    def onchange_discount_approved(self):
        self.discount_approved_by = lambda self: self.env.user




