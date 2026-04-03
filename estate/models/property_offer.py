from odoo import fields,models

class PropOfferModel(models.Model):
    _name = "propoffer.model"
    _description = "Property Offer Model"

    price=fields.Float()
    status=fields.Selection([('accepted','Accepted'),('refused','Refused')],copy=False)
    partner=fields.Many2one("res.partner",string="Customer", required=True)
    property=fields.Many2one("property.model",string="Property")
    validity=fields.Integer(default=7)
    create_date=fields.Date(string="Create Date")
    date_deadline=fields.Date(string="Deadline")

    # @api.depends('offers')
    # def _compute_best_price(self):
    #      l=[]
    #      for record in self:
    #          for offer in record.offers:
    #             l.append(offer.price)
    #          record.best_price=max(l)

    # @api.depends("create_date","validity")
    # def _compute_deadline(self):
    #     for record in self:
    #         if record.create_date and record.validity:
