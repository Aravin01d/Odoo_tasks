import datetime

from odoo import api,fields, models
from odoo.exceptions import ValidationError

class EmployeeLoan(models.Model):
    _name = 'employee.loan'
    _description = 'Employee Loan'

    name = fields.Char(string="Name",default="New",readonly=True)
    employee_id = fields.Many2one('hr.employee',string="Employee ID")
    loan_amount = fields.Float(string="Loan Amount")
    installment_count = fields.Integer(string="Installment Count")
    state = fields.Selection([
        ("draft", "Draft"),
        ("approved","Approved"),
        ("ongoing","Ongoing"),
        ("paid","Paid")
    ],
    string = "State",
    default = "draft",)
    loan_line_ids = fields.One2many("employee.loan.line","loan_id",string="Loan Lines")
    installment_amount = fields.Integer(string="Installment Amount")
    total_payable = fields.Float(string="Total Payable",compute = "_compute_total_payable", store=True)
    loan_line_count = fields.Integer(string="Loan Line Count",compute="_compute_loan_line_count", store=True)
    paid_amount=fields.Float(string="Paid Amount", compute="_compute_paid_amount", store=True)
    balance_amount=fields.Float(string="Balance Amount", compute="_compute_balance_amount", store=True)

    @api.onchange("loan_amount","installment_count")
    def _onchange_loan_amount(self):
        la = self.loan_amount
        ic = self.installment_count
        if la and ic:
            self.installment_amount = la/ic

    @api.depends('loan_amount')
    def _compute_total_payable(self):
        print("In compute")
        for record in self:
            la=record.loan_amount
            print(la)
            if la:
                record.total_payable = la

    @api.depends('loan_line_ids')
    def _compute_loan_line_count(self):
        for record in self:
            record.loan_line_count = self.env['employee.loan.line'].search_count([("loan_id","=",record.name)])

    @api.depends('loan_line_ids.paid')
    def _compute_paid_amount(self):
        lines=self.env['employee.loan.line'].search([('loan_id','=',self.name),('paid','=',True)])
        amounts=lines.mapped("amount")
        print(sum(amounts))
        self.paid_amount=sum(amounts)

    @api.depends('loan_line_ids.paid')
    def _compute_balance_amount(self):
        print("ok")
        lines=self.env['employee.loan.line'].search([('loan_id','=',self.name),('paid','=',False)])
        amounts = lines.mapped("amount")
        print(sum(amounts))
        self.balance_amount = sum(amounts)

    def action_view_installments(self):
        return{
            "type": "ir.actions.act_window",
            "name":"Installments",
            "res_model": "employee.loan.line",
            "view_mode": "list",
            "domain":[("loan_id",'=',self.name)]
        }

    @api.model_create_multi
    def create(self, vals):
        for rec in vals:
            code = self.env['ir.sequence'].next_by_code('employee.loan')
            rec['name'] = code
        res = super().create(vals)
        return res

    def generate_installments(self):
        loan_line_records = self.env['employee.loan.line'].search(
            [('loan_id', '=', self.name)])
        for i in range(self.installment_count):
                records_vals={
                    'loan_id':self.id,
                    'date':datetime.datetime.today(),
                    'amount':self.installment_amount,
                    'paid':False,
                }
                if not loan_line_records:
                    self.env['employee.loan.line'].create(records_vals)
                else:
                    self.env['employee.loan.line'].write(records_vals)
        self.state = "ongoing"

    def pay_installment(self):
        lines=self.env["employee.loan.line"].search([('loan_id','=',self.name),('paid','=',False)],limit=1)
        if lines:
            lines.paid=True
        all_lines=self.env["employee.loan.line"].search([('loan_id','=',self.name)])
        paid_list=all_lines.mapped("paid")
        if False not in paid_list:
            self.state="paid"

    def action_draft(self):
        self.state = "draft"

    def action_approved(self):
        if self.loan_amount<0:
            raise ValidationError("Loan Amount cannot be negative")
        self.state = "approved"

    def action_ongoing(self):
        self.state = "ongoing"

    def action_paid(self):
        self.state = "paid"

