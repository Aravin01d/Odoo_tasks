from odoo import fields,models

class Publishers(models.Model):
    _name = 'publishers.model'
    _description = 'Publishers Model'

    name = fields.Char(string="Name")
    address=fields.Char(string="Address")
    publisher_book_ids = fields.One2many('books.model', "publisher_id", string="Books")
