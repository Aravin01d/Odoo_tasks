from odoo import fields, models

class PropTypeModel(models.Model):
    _name = "proptype.model"
    _description = "Property Type Model"

    name = fields.Char(required=True)