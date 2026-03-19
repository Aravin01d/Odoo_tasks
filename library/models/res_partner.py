from odoo import fields, models, api

class ResPartner(models.Model):
    _inherit = 'res.partner'
    book_count=fields.Integer(string="Books", compute='compute_book_count', default=0)
    late_returns = fields.Integer(string="Late Returns", compute='compute_late_returns')
    total_penalty=fields.Float(string="Total Penalty", compute= 'compute_total_penalty')
    books_allowed=fields.Integer(string="Books Allowed")
    max_late_returns=fields.Integer(string="Maximum Late Returns", compute='compute_max_late_returns')

    product_ids=fields.Many2many('product.product', string= "Products")

    def compute_book_count(self):
        for record in self:
            record.book_count=self.env['checkouts.model'].search_count([('member_id', '=', self.id)])

    def action_view_library_records(self):
        return{
            'type':'ir.actions.act_window',
            'name':'Books',
            'view_mode':'list',
            'res_model':'checkoutlines.model',
            'domain':[('member_id','=',self.id)],
            'context':"{'create':False}"
        }

    def compute_late_returns(self):
        for record in self:
            record.late_returns=self.env['checkouts.model'].search_count([('member_id', '=', self.id),('is_late','=',True)])

    def action_view_late_returns(self):
        return{
            'type': 'ir.actions.act_window',
            'name': 'Late Returns',
            'view_mode': 'list',
            'res_model': 'checkouts.model',
            'domain': [('member_id', '=', self.id)],
            'context': "{'create':False}"
        }

    def compute_total_penalty(self):
        for record in self:
            records=self.env['checkouts.model'].search([('member_id','=',self.id)])
            l=[]
            for rec in records:
                l.append(rec.penalty)
            record.total_penalty = sum(l)

    def action_view_total_penalty(self):
        return{
            'type': 'ir.actions.act_window',
            'name': 'Total Penalty',
            'view_mode': 'list',
            'res_model': 'checkouts.model',
            'domain': [('member_id', '=', self.id)],
            'context': "{'create':False}"
        }

    @api.model_create_multi
    def create(self, vals):
        x = int(self.env['ir.config_parameter'].sudo().get_param('library.max_books'))
        # print(x)10.00
        for rec in vals:
            rec['books_allowed']=x
        return super().create(vals)

    def compute_max_late_returns(self):
        mlr=int(self.env['ir.config_parameter'].sudo().get_param('library.max_late_returns'))
        for rec in self:
            rec.max_late_returns = mlr

    def compute_books_allowed(self):
        ba=int(self.env['ir.config_parameter'].sudo().get_param('library.max_books'))
        for rec in self:
            rec.books_allowed=ba

    # def action_recalculate(self):
    #
    #     product_threshold = float(self.env['ir.config_parameter'].sudo().get_param('library.product_threshold'))
    #     orders=self.env['sale.order'].search([("partner_id",'=',self.id)])
    #     order_lines=self.env['sale.order.line'].search([('order_partner_id','=',self.id)])
    #     dict = {}
    #     for i in order_lines:
    #         qts=i.product_uom_qty
    #         products=i.product_id.id
    #         if products in dict:
    #             dict[products] += qts
    #         else:
    #             dict[products] = qts
    #     top_products=[k for k in dict if dict[k]>=product_threshold]
    #     for i in top_products:
    #         self.update({
    #             'product_ids':[(fields.Command.link(i))]
    #         })
    #
    # def action_add_so(self):
    #
    #     products_list=[]
    #     for i in self.product_ids:
    #         products_list+=[(fields.Command.create({
    #             "product_id": i.id
    #         }))]
    #     order_data={
    #         'partner_id': self.id,
    #         'order_line':[x for x in products_list]
    #     }
    #     new_sale_order=self.env['sale.order'].create(order_data)