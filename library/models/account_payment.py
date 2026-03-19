from odoo import fields, models
from odoo.addons.test_convert.tests.test_env import record

class AccountPayment(models.TransientModel):
    _inherit = 'account.payment.register'

    def action_create_payments(self):
        print("Move id :",self.line_ids.move_id.checkout_id.book_ids.book_line_id)
        for record in self:
            print("ABCD")
            for i in record.line_ids.move_id.checkout_id.book_ids.book_line_id:
                print(i)
                i.status='available'
            #     print(i.status)
            # record.checkout_id.book_ids.book_line_id.status='available'
        return super().action_create_payments()

# .checkout_id.book_ids.book_line_id.status