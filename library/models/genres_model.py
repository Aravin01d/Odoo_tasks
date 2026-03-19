from  odoo import fields,models

class GenresModel(models.Model):
    _name = 'genres.model'
    _description = 'Genres Model'
    _rec_name = 'genre_name'

    genre_name = fields.Char(string="Genres")
    book_ids=fields.Many2many('books.model',string="Books")
