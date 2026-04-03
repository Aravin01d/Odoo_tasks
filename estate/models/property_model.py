from datetime import timedelta
from email.policy import default
from  odoo import api
from openpyxl.styles.builtins import total

from odoo.tools import date_utils

from odoo import fields, models

class PropertyModel(models.Model):
    _name = "property.model"
    _description = "Property Model"

    name = fields.Char(required=True)
    description=fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False,default=date_utils.add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True)
    # best_price=fields.Float(compute="_compute_best_price")
    selling_price = fields.Float(readonly=True,copy=False)
    bedrooms=fields.Integer(default=2)
    living_area=fields.Integer()
    facades=fields.Integer()
    garage=fields.Boolean()
    garden=fields.Boolean()
    garden_area=fields.Integer()
    garden_orientation=fields.Selection([("north","North"),("south","South"),("east","East"),("west","West")])
    total_area=fields.Float(string="Total Area",compute="_compute_total_area")
    active=fields.Boolean(default=False)
    state=fields.Selection([("new","New"),("received","Offer received"),("accepted","Offer accepted"),("sold","Sold"),("cancelled","Cancelled")],default="new",required=True,copy=False)
    property_type=fields.Many2one("proptype.model",string="Property Type")
    buyer=fields.Many2one("res.partner",string="Customer", copy=False)
    seller=fields.Many2one("res.partner",string="SalesPerson", default=lambda self: self.env.user)
    tags=fields.Many2many("proptag.model",string="Tags")
    offers=fields.One2many("propoffer.model",'property',copy=False)

    @api.depends('garden')
    def _onchange_garden(self):
        for record in self:
            if record.garden==True:
                record.garden_area=10
            else:
                record.garden_area=0

    @api.depends('living_area','garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area=record.living_area + record.garden_area
