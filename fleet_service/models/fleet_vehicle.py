from odoo import api, fields, models

class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    service_blocked = fields.Boolean(string="Service Blocked")