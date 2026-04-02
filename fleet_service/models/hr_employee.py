from odoo import api, fields, models

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    is_available_technician = fields.Boolean(string="Is Available Technician")
    vehicle_ids = fields.Many2many("fleet.vehicle",string="Vehicle IDs")