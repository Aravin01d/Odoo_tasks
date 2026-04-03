from odoo import fields,models

class PropTagModel(models.Model):
    _name = "proptag.model"
    _description = "Property Tag Model"

    name = fields.Char(required=True)
