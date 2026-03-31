from itertools import count

from odoo import api, fields, models, tools

class FleetServiceOrder(models.Model):
    _name = 'fleet.service.order'
    _description = 'Fleet Service Order'

    name = fields.Char(string="Fleet Service Order", default="New")
    vehicle_id = fields.Many2one("fleet.vehicle",
                                 string="Vehicle")
    technician_id=fields.Many2one("hr.employee",string="Technician")
    service_date=fields.Datetime(string="Service Date")
    state=fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('in progress', 'In Progress'),
        ('done', 'Done'),


        ('cancel', 'Cancelled'),],
        string='Status',
        default='draft',
    )
    part_ids = fields.One2many("fleet.service.order.part","order_id",string="Parts")
    checklist_ids=fields.One2many("fleet.service.order.checklist","order_id",string="Checklists")
    parts_total=fields.Float(string="Total Parts",compute="_compute_parts_total",store=True)
    labour_cost=fields.Float(string="Labour Cost")
    grand_total=fields.Float(string="Grand Total",compute="_compute_grand_total",store=True)
    checklist_progress=fields.Float(string="Checklist Progress",compute="_compute_checklist_progress",store=True)

    @api.model_create_multi
    def create(self, vals):
        """Function to create employee id sequence."""
        for rec in vals:
            code = self.env['ir.sequence'].next_by_code('fleet.service.order')
            rec['name'] = code
        res = super().create(vals)
        return res

    @api.depends("part_ids")
    def _compute_parts_total(self):
        price_subtotal=0.0
        l=[]
        # sum of qty * unit_price of all part ids.
        lines=self.env['fleet.service.order.part'].search([('order_id','=',self.id)])
        for rec in lines:
            price_subtotal=rec.quantity*rec.unit_price
            l.append(price_subtotal)
            # print(price_subtotal)
        print(sum(l))
        self.parts_total=sum(l)

    @api.depends("part_ids")
    def _compute_grand_total(self):
        print("yeah")
        for rec in self:
            rec.grand_total=rec.parts_total+rec.labour_cost

    @api.depends("checklist_ids")
    def _compute_checklist_progress(self):
        # count=0

        lines = self.env['fleet.service.order.checklist'].search_count(
            [('order_id', '=', self.id),('is_done', '=', True)])
        print(lines)

        total_lines=self.env['fleet.service.order.checklist'].search_count(
            [('order_id', '=', self.id)])
        if self.checklist_ids:
            self.checklist_progress = (lines/total_lines)*100
        else:
            self.checklist_progress=0
        # count of done checklist items/total checklist items *100

