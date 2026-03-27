from odoo import api, fields, models

class EmployeeLoanLine(models.Model):
    """Employee Loan Line Model"""
    _name = 'employee.loan.line'
    _description='Employee Loan Line'

    loan_id = fields.Many2one("employee.loan",string="Loan ID",readonly=True)
    date = fields.Datetime(string="Date")
    amount = fields.Float(string="Amount")
    paid = fields.Boolean(string="Paid")
