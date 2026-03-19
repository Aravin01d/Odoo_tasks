from odoo import models,fields,api

class CheckoutLinesModel(models.Model):
    _name='checkoutlines.model'
    _description='Checkout Lines Model'

    member_id=fields.Many2one(related='checkout_line_id.member_id',string="Member")
    checkout_line_id=fields.Many2one("checkouts.model",string="checkout line id")
    book_line_id=fields.Many2one("books.model",string="Books")
    price=fields.Float(related="book_line_id.price",string="Price")
    status=fields.Selection(related="book_line_id.status",string="Status")
    author_id=fields.Many2one(related="book_line_id.author_id",string="Author")
    genre_ids=fields.Many2many(related='book_line_id.genre_ids',string="Genre")
    checkout_date=fields.Datetime("Checkout Date",related="checkout_line_id.checkout_date")
    return_date=fields.Datetime(related="checkout_line_id.return_date",string="Return Date")
    is_late=fields.Boolean(related="checkout_line_id.is_late", string="Is Late")

