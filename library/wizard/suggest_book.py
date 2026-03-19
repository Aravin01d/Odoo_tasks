from odoo import fields,models

class SuggestBookModel(models.TransientModel):
    _name = 'suggestbook.model'
    _description = 'Suggest Books'
    name_ids=fields.Many2many('books.model',string="Suggest Book")
    author_id=fields.Many2one(related='name_ids.author_id',string="Author")
    genre_ids=fields.Many2many(related='name_ids.genre_ids',string="Genre")
    checkout_id=fields.Many2one("checkouts.model",string="Checkout")

    def suggest_book(self):
        print(self.name_ids.ids)
        for i in self.name_ids.ids:
            self.checkout_id.update({
                'book_ids':[(fields.Command.create({'book_line_id':i}))]
            })
