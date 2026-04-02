from odoo import fields,models

class ChecklistType(models.Model):
    _name = "checklist.type"
    _description = "Checklist Type"

    name=fields.Char(string="Name")
