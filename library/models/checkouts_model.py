from datetime import timedelta
from itertools import product
from re import search

from odoo import fields,models,Command,api,_
import datetime

from odoo.addons.test_convert.tests.test_env import record
from odoo.exceptions import ValidationError, UserError, AccessError
from odoo.tools import date_utils

class CheckoutsModel(models.Model):

    _name = 'checkouts.model'
    _description = 'Checkouts Model'
    _rec_name = 'checkout_id'
    _inherit=['mail.thread','mail.activity.mixin']

    member_id=fields.Many2one("res.partner",string="Member",required=True)
    user_id=fields.Many2one("res.users",default=lambda self: self.env.user)
    number= fields.Char(related="member_id.phone",string="Phone Number", readonly=False)
    email=fields.Char(related="member_id.email",string="Email Address")
    checkout_id=fields.Char("Checkout ID",readonly=True,tracking=True,copy=False,default="New",required=True)
    checkout_date=fields.Datetime(string="Checkout Date",tracking=True)
    due_date=fields.Datetime(string="Due Date")
    return_date=fields.Datetime(string="Return Date",tracking=True)
    status=fields.Selection(
[('draft','Draft'),
        ('checked out','Checked 0ut'),
        ('returned', 'Returned'),
        ('overdue','Over Due'),
        ('cancelled','Cancelled')],
        string="Status",
        default="draft"
        )
    penalty = fields.Float(string="Penalty",store=True,default=0.0)
    book_ids=fields.One2many("checkoutlines.model","checkout_line_id",string="Books", required=True)
    rem_days=fields.Integer(string="Remaining Days", compute="_compute_rem_days",store=True)
    is_late=fields.Boolean(string=" Is Late",compute="_compute_is_late",store=True)
    invoice_id=fields.Many2one("account.move",string="Invoice ID")
    payment_state=fields.Selection(related="invoice_id.payment_state",string="Payment State")


    @api.model_create_multi
    def create(self, vals):
        for rec in vals:
            code=self.env['ir.sequence'].next_by_code('checkouts.model')
            rec['checkout_id']=code
        res=super().create(vals)
        return res

    def action_draft(self):
        records = self.filtered(lambda s: s.status in ['returned', 'overdue','cancelled','checked out','draft'])
        return records.write({
            'status': 'draft'
        })

    def action_confirm(self):
        borrow_days = int(self.env['ir.config_parameter'].sudo().get_param('library.borrow_days'))
        mlr = self.member_id.max_late_returns
        lr = self.member_id.late_returns
        if lr == mlr:
            raise ValidationError("Late return limit exceeded")
        elif lr == mlr - 1:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Warning',
                    'message': f'Late returns increasing.',
                    'type': 'warning',
                    'sticky': False,  # Auto-dismiss after a few seconds
                }
            }
        for record in self:
            x=self.search_count([('member_id', '=', self.member_id),'|',('status','=','overdue'),('status','=','checked out')])
            print(x)
            if x>0:
                raise ValidationError("Checkout already exists")
            else:
                record.checkout_date=datetime.datetime.today()
                record.due_date=date_utils.add(record.checkout_date,days=borrow_days).date()
                record.status = 'checked out'
                record.book_ids.book_line_id.status='unavailable'

                books_by_author = self.env['books.model'].search(
                    ['&', ('status', '=', 'available'), ('author_id', '=', self.book_ids.book_line_id.author_id)])
                books_by_genre=self.env['books.model'].search(
                    ['&', ('status', '=', 'available'),('genre_ids', '=', self.book_ids.book_line_id.genre_ids)])
                all_books_available=self.env['books.model'].search(
                    [('status','=','available')])
                if all_books_available:
                    all_books=max(all_books_available.mapped('return_count'))
                    all_avail_books=self.env['books.model'].search(
                        ['&', ('status', '=', 'available'),('return_count','=',all_books)])

                    search_books=books_by_author.ids+books_by_genre.ids+all_avail_books.ids

                    return {
                        'name': _('Suggest Book'),
                        'type': 'ir.actions.act_window',
                        'res_model': 'suggestbook.model',
                        'view_mode': 'form',
                        'view_type': 'form',
                        'target': 'new',
                        'context':{
                                    'default_name_ids': search_books,
                                    'default_checkout_id':self.id
                                   }
                    }
                else:
                    pass


    def action_return(self):
        # print("product record id:",self.env.ref('library.penalty_product').id)
        for record in self:
            record.status = 'returned'
            record.return_date = datetime.datetime.now()
            invoice_line_list=[]
            for i in record.book_ids:
                invoice_line_list+=[(fields.Command.create({
                        "product_id": i.book_line_id.product_id,
                        "price_unit": i.book_line_id.price}))]
            # print('books:', record.book_ids.book_line_id.product_id)
            if record.penalty>0:
                invoice_line_list+=[(Command.create({
                    "product_id": self.env.ref('library.penalty_product').id,
                    'price_unit': self.penalty
                }))]
            print('invoice_line list :', invoice_line_list)

            # for i in invoice_line_list:
                # print(i)
            # print(x for x in invoice_line_list)
            invoice_data= {
                "move_type": 'out_invoice',
                "partner_id": self.member_id.id,
                "invoice_date": datetime.date.today(),
                    "line_ids": [x for x in invoice_line_list]
            }
            print("Invoice Data:",invoice_data)
            new_invoice=self.env['account.move'].create(invoice_data)
            record.invoice_id=new_invoice.id
            record.invoice_id.checkout_id=self.id

        # print(self.env['account.move'].search([('name','=',self.checkout_id)]))
        # print(self.invoice_id.payment_state)

        for record in self.book_ids.book_line_id:
            record.return_count+=1

    def action_cancel(self):
        for record in self:
            record.status='cancelled'
        record.book_ids.book_line_id.status = 'available'
        # if self.payment_state == 'paid':
        #     record.book_ids.book_line_id.status = 'available'
        #     print("Nice")
        # print(self.book_ids)

    @api.depends("due_date")
    def overdue_checking(self):
        members=self.search([('status','=','checked out')])
        penalty_amount = float(self.env['ir.config_parameter'].sudo().get_param('library.penalty_amount'))
        for rec in members:
            if rec.due_date and rec.due_date < datetime.datetime.today():
                rec.status = 'overdue'
                overdue_days=datetime.datetime.today() - rec.due_date
                seconds=overdue_days.total_seconds()
                hours=seconds // 3600
                penalty_fee=hours*penalty_amount
                rec.penalty=penalty_fee

    @api.depends("due_date","return_date")
    def _compute_is_late(self):
        for record in self:
            if record.due_date and record.return_date:
                if record.due_date < record.return_date:
                    record.is_late=True
                else:
                    record.is_late=False

    def due_date_reminder(self):
        reminder_days = int(self.env['ir.config_parameter'].sudo().get_param('library.reminder_days'))
        print(reminder_days)
        template = self.env.ref('library.email_template_days_reminder', raise_if_not_found=False)
        members = self.search([('status', '=', 'checked out')])
        print(members)
        for rec in members:
            if rec.due_date:
                due_date_ = rec.due_date.date()
            rem_days = due_date_ - timedelta(days=reminder_days)
            print('rem days :', rem_days)
            if rem_days == datetime.date.today():
                template.send_mail(rec.id, force_send=False)

    def overdue_notice(self):
        template = self.env.ref('library.email_template_overdue_notice')
        members = self.search([('status', '=', 'overdue')])
        for rec in members:
            template.send_mail(rec.id, force_send=False)

    @api.depends("due_date")
    def _compute_rem_days(self):
        reminder_days = int(self.env['ir.config_parameter'].sudo().get_param('library.reminder_days'))
        members = self.search([('status', '=', 'checked out')])
        for rec in members:
            if rec.due_date:
                x=rec.due_date - timedelta(days=reminder_days)
                y = rec.due_date - x
                rec.rem_days=y.days

    @api.constrains("book_ids")
    def block_borrow(self):
        books_allowed=self.member_id.books_allowed
        l = []
        for i in self.book_ids:
            l.append(i)
        x=len(l)
        if  x > books_allowed:
            raise ValidationError("Borrow limit exceeded")

    def action_view_invoice(self):
        return {
            'name': _('Book Return Invoice'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.move',
            'type': 'ir.actions.act_window',
            'res_id': self.invoice_id.id,
        }

        # for record in self:
        #     if record.payment_state == 'paid':
        #         print("yes")
        #         record.book_ids.book_line_id.status = 'available'
        #     if record.payment_state == 'not_paid':
        #         print("NO")

    def action_show(self):
        # TOTAL CHECKOUTS OF CURRENT MEMBER
        print("Total number of checkouts of current member: ",self.search_count([('member_id', '=', self.member_id)]))

        # ALL CUSTOMER NAMES
        print("All customers:",self.member_id.search([]).mapped('name'))

        # COUNT OF TOTAL CUSTOMERS
        print("Count of all customers:",self.member_id.search_count([]))

        #CHANGING CUSTOMER NUMBERS
        customers=self.member_id.search([])
        customers.write({'phone':999})
        for rec in customers:
            if rec.phone:
                rec.write({'phone': 9999})
            if not rec.phone:
                rec.write({'phone': 777})

        #CLEARING ORDER LINE
        for record in self:
            if record:
                self.update({
                    'book_ids':[(fields.Command.clear())]
            })
                self.update({
                    'book_ids':[(fields.Command.create({
                        'book_line_id': 5
                    }))]
                })

        # AUTHOR OR GENRE CHECKING
        book_line=self.book_ids.book_line_id
        for rec in book_line:
            author=rec.author_id
            genre=rec.genre_ids
            if not author or not genre:
                raise ValidationError("All books does not have proper data")
