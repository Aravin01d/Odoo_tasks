from odoo import models, fields, api

class SettingsModel(models.TransientModel):
    _inherit = 'res.config.settings'

    borrow_days=fields.Integer(string='Maximum Borrowing Days',
                               help="Set the maximum borrowing days for a book",
                               config_parameter="library.borrow_days")

    reminder_days=fields.Integer(string='Reminder Days',
                                 help="Set the reminder days before a book is due",
                                 config_parameter="library.reminder_days")

    penalty_amount=fields.Float(string="Penalty Amount",
                                help="Set the penalty charged for each hour a book is overdue",
                                config_parameter="library.penalty_amount")

    max_books=fields.Integer(string="Maximum Books", config_parameter="library.max_books")

    max_late_returns=fields.Integer(string="Maximum Late Returns", config_parameter="library.max_late_returns")

    product_threshold=fields.Float(string="Product Threshold", help="Set the product threshold for customer", config_parameter="library.product_threshold")
