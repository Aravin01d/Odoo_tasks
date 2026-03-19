from itertools import count

from odoo import fields, models, api

class BooksModel(models.Model):
    _name = 'books.model'
    _description = 'Books Model'
    _rec_name = 'title'

    user_id=fields.Many2one('res.users',default=lambda self: self.env.user.id)
    title= fields.Char(string="Title",required=True,_compute='search_book')
    cover_image = fields.Image(string="Cover Image")
    book_id = fields.Char(string="Book ID",
                          copy=False,
                          default="New",
                          readonly=True,
                          required=True
                          )
    product_id = fields.Char(string="Product ID")
    author_id=fields.Many2one("authors.model",string="Author")
    genre_ids= fields.Many2many("genres.model", string="Genre Types")
    publisher_id=fields.Many2one("publishers.model",string="Publishers")
    isbn=fields.Char(string="ISBN", required=True)
    price=fields.Float(string="Price")
    cost=fields.Float(string="Cost")
    status=fields.Selection([('available','Available'),('unavailable','Unavailable'),('coming soon','Coming Soon')],string="Status")
    return_count=fields.Integer(string="Return Count")
    # sale_orders_id = fields.Many2one('sale.order', string="Sale Orders")

    _unique_isbn = models.Constraint('UNIQUE(isbn)', "ISBN must be unique")

    @api.model_create_multi
    def create(self, vals):
        print(self.genre_ids)
        for rec in vals:
            code = self.env['ir.sequence'].next_by_code('books.model')
            rec['book_id'] = code
        res = super().create(vals)
        for record in res:
            x=self.env['product.product'].create({
                'name': record.title,
                'type': 'service',
                'list_price': record.price,
            })
            record.product_id = x.id
        return res
    # def create_product(self):
    #     return

