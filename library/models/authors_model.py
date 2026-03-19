from odoo import fields,models

class AuthorsModel(models.Model):
    _name = 'authors.model'
    _description = 'Books by Author'
    _rec_name = 'author_name'
    book_ids=fields.One2many("books.model","author_id",string="Books")
    author_name=fields.Char(string="Author")
    description = fields.Char(string="Description")

