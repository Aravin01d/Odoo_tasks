from odoo import fields,models

class FleetServiceOrderChecklist(models.Model):
    _name = 'fleet.service.order.checklist'
    _description = 'Fleet Service Order Checklist'

    order_id = fields.Many2one("fleet.service.order",string="Order ID")
    task_name=fields.Char(string="Task Name")
    is_done=fields.Boolean(string="Is Done")
    note=fields.Text(string="Note")