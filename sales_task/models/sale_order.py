from odoo import fields, models, api, _

from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = ['sale.order']

    delivery_remark = fields.Text(string="Delivery Remark")
    is_urgent_delivery = fields.Boolean(string="Is Urgent Delivery")
    preferred_delivery_time = fields.Selection([
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon'),
        ('evening', 'Evening'),
    ],
    string="Preferred Delivery Time")
    discount_approved = fields.Boolean(string="Discount Approved")
    discount_approved_by = fields.Many2one("res.users",string="Discount Approved By",readonly=True)

    def action_approve_discount(self):
        for rec in self:
            # print(rec.order_line.mapped('discount'))
            discounts = rec.order_line.mapped('discount')
            res = any(value > 0 for value in discounts)
            if res == False:
                raise ValidationError("Atleast one discount needed.")
            rec.discount_approved = True
            rec.discount_approved_by = self.user_id
            self.message_post(body=_("Discount approved by %s",self.user_id.name))

    # def message_post(self, body):
    #     pass
