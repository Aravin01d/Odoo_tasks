from odoo import fields, models, _
import io
import json
from odoo.tools import json_default
import xlsxwriter

class BookReportWizard(models.TransientModel):
    _name = 'book.report.wizard'
    _description = 'Book Report Wizard'

    checkout_id = fields.Many2one("checkouts.model", string="Checkout")
    member_id=fields.Many2one("res.partner", string="Member")
    book_id=fields.Many2one("books.model",string="Book")
    genre_id=fields.Many2one("genres.model",string="Genre")
    checkout_date = fields.Date(string="Checkout Date")
    return_date=fields.Date(string="Return Date")
    sort_by=fields.Selection([('checkout_date','Checkout Date'),('due_date','Due Date')],string="Sort By")
    order_by=fields.Selection([('ascending','Ascending'),('descending','Descending')],string="Order By")

    # checkout_dte=fields.Datetime(string="Checkout Date")
    # return_dte=fields.Datetime(string="Return Date")
    def view_book_report_wizard(self):
        return {
            'name': _('Book Reports'),
            'type': 'ir.actions.act_window',
            'res_model': 'product.menu',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
        }

    def action_print_report(self):
        sql_query = """
        SELECT cm.checkout_id, cm.member_id, cl.book_line_id,am.author_name,bm.title,gm.genres_model_id,gr.genre_name,rs.name,
        CAST(checkout_date AS DATE) AS checkout_dte,
        CAST(return_date AS DATE) AS return_dte,
        CAST(due_date AS DATE) AS due_dte
         from checkouts_model as cm
         INNER JOIN res_partner as rs on rs.id = cm.member_id
         INNER JOIN checkoutlines_model as cl ON cm.id = cl.checkout_line_id
         INNER JOIN books_model as bm ON cl.book_line_id=bm.id 
         INNER JOIN authors_model as am on am.id=bm.author_id
         INNER JOIN books_model_genres_model_rel as gm on bm.id=gm.books_model_id
         INNER JOIN genres_model as gr on gr.id=gm.genres_model_id 
        """
        l=[]
        if self.member_id:
            sql_query+=""" WHERE cm.member_id = %s"""
            l.append(self.member_id.id)
        if self.book_id:
            sql_query +=""" AND bm.id = %s"""
            l.append(self.book_id.id)
        if self.genre_id:
            sql_query +=""" AND gr.id = %s"""
            l.append(self.genre_id.id)
        if self.checkout_date:
            sql_query +=""" AND CAST(checkout_date AS DATE) = %s"""
            l.append(self.checkout_date)
        if self.return_date:
            sql_query +=""" AND CAST(return_date AS DATE) = %s"""
            l.append(self.return_date)
        if self.sort_by=="checkout_date" and self.order_by=="ascending":
            sql_query+=""" ORDER BY checkout_dte ASC"""
            # l.append(self.checkout_date)
        if self.sort_by=="due_date" and self.order_by=="ascending":
            sql_query+=""" ORDER BY due_dte ASC"""
            # l.append(self.return_date)
        if self.sort_by=="checkout_date" and self.order_by=="descending":
            sql_query+=""" ORDER BY checkout_dte DESC"""
            # l.append(self.checkout_date)
        if self.sort_by=="due_date" and self.order_by=="descending":
            sql_query+=""" ORDER BY due_dte DESC"""
            # l.append(self.return_date)

        print("THE LIST IN PDF",l)
        print(type(self.checkout_date))
        self.env.cr.execute(sql_query, tuple(l))
        report=self.env.cr.dictfetchall()
        data = {'date': self.read()[0],'report': report}
        print("data:",data)
        return self.env.ref('library.action_book_report_template').report_action(self.ids,data=data)

    def action_print_xlsx_report(self):
        data={
            'checkout_id':self.checkout_id,
            'member_id':self.member_id.name,
            'book_id':self.book_id.title,
            'genre_id':self.genre_id.genre_name,
            'checkout_date':self.checkout_date,
            'return_date':self.return_date,
            'sort_by':self.sort_by,
            'order_by':self.order_by
        }
        print("You reached print xlsx function")
        return{
            'type':'ir.actions.report',
            'data':{
                'model':'book.report.wizard',
                'options':json.dumps(data, default=json_default),
                'output_format':'xlsx',
                'report_name':'Library Excel Report',
                    },
            'report_type':'xlsx',
        }

    def get_xlsx_report(self,data, response):
        print("Data:",data)
        sql_query = """
        SELECT cm.checkout_id, cm.member_id, cl.book_line_id,am.author_name,bm.title,gm.genres_model_id,gr.genre_name,rs.name,
        CAST(checkout_date AS DATE) AS checkout_dte,
        CAST(return_date AS DATE) AS return_dte,
        CAST(due_date AS DATE) AS due_dte
         from checkouts_model as cm
         INNER JOIN res_partner as rs on rs.id = cm.member_id
         INNER JOIN checkoutlines_model as cl ON cm.id = cl.checkout_line_id
         INNER JOIN books_model as bm ON cl.book_line_id=bm.id 
         INNER JOIN authors_model as am on am.id=bm.author_id
         INNER JOIN books_model_genres_model_rel as gm on bm.id=gm.books_model_id
         INNER JOIN genres_model as gr on gr.id=gm.genres_model_id 
        """
        l=[]
        if data['member_id']:
            sql_query += """ WHERE rs.name = %s"""
            l.append(data['member_id'])
            print("DID LIST GET APPEND",l)
        if data['book_id']:
            sql_query += """ AND bm.title = %s"""
            l.append(data['book_id'])
        if data['genre_id']:
            sql_query += """ AND gr.genre_name = %s"""
            l.append(data['genre_id'])
        if data['checkout_date']:
            sql_query += """ AND CAST(checkout_date AS DATE) = %s"""
            l.append(data['checkout_date'])
        if data['return_date']:
            sql_query += """ AND CAST(return_date AS DATE) = %s"""
            l.append(data['return_date'])
        if data['sort_by'] == "checkout_date" and data['order_by'] == "ascending":
            sql_query += """ ORDER BY checkout_dte ASC"""
            # l.append(self.checkout_date)
        if data['sort_by'] == "due_date" and data['order_by'] == "ascending":
            sql_query += """ ORDER BY due_dte ASC"""
            # l.append(self.return_date)
        if data['sort_by'] == "checkout_date" and data['order_by'] == "descending":
            sql_query += """ ORDER BY checkout_dte DESC"""
            # l.append(self.checkout_date)
        if data['sort_by'] == "due_date" and data['order_by'] == "descending":
            sql_query += """ ORDER BY due_dte DESC"""
            # l.append(self.return_date)

        print("THE LIST:",l)
        self.env.cr.execute(sql_query, tuple(l))
        report = self.env.cr.dictfetchall()
        docs={'report':report}

        # info = {'date': self.read()[0], 'Docs': docs}

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        # workbook = xlsxwriter.Workbook('library_report.xlsx')
        sheet = workbook.add_worksheet()
        sheet.set_column(1,20,20)
        print("sheet:",sheet)
        print("Docs:",docs)

        head=workbook.add_format(
            {'align':'center',
             'bold':True,
             'font_size':'20px'}
        )

        date_format = workbook.add_format({'num_format':'dd-mm-yyyy','align':'center'})

        bold = workbook.add_format({'bold': True,'align':'center'})

        txt=workbook.add_format(
            {'font_size':'10px',
             'align':'center'
             }
        )
        sheet.merge_range(1,3 ,1,7,"Excel Report", head)
        row=3
        col=3
        if data['member_id']:
            # print("Partner:",data['member_id'])
            sheet.write(row, col, 'Member', bold)
            col+=1
            sheet.write(row, col,data['member_id'], txt)
        if data['book_id']:
            row += 1
            sheet.write(row, 3, 'Book', bold)
            sheet.write(row, 4,data['book_id'], txt)
        if data['genre_id']:
            row += 1
            sheet.write(row, 3, 'Genre', bold)
            sheet.write(row, 4, data['genre_id'], txt)
        if data['checkout_date']:
            row+=1
            sheet.write(row, 3, 'Checkout Date', bold)
            sheet.write(row, 4,data['checkout_date'], txt)
        if data['return_date']:
            row+=1
            sheet.write(row, 3,'Return Date', bold)
            sheet.write(row, 4,data['return_date'], txt)

        row=10
        col=3

        sheet.write(row,col, "Reference ID", bold)
        if data['book_id']==False:
            col+=1
            print("No book selected")
            sheet.write(row,col, "Book",bold)
        if data['member_id']==False:
            col+=1
            print("Member not selected")
            sheet.write(row, col, "Member", bold)
        # sheet.write(row,col+2,"Author", bold)
        if data['genre_id']==False:
            col+=1
            print("Genre not selected")
            sheet.write(row,col, "Genre", bold)
        if data['checkout_date']==False:
            col+=1
            print("Checkout Date not selected")
            sheet.write(row,col, "Checkout Date", bold)
        if data['return_date']==False:
            col+=1
            print("Return Date not selected")
            sheet.write(row, col, "Return Date", bold)

        row+=1
        col=3

        for i in docs['report']:
                sheet.write(row,col,i['checkout_id'], txt)

                if data['book_id'] == False:
                    col+=1
                    sheet.write(row,col,i['title'], txt)
                if data['member_id'] == False:
                    col+=1
                    sheet.write(row,col,i['name'], txt)

                # sheet.write(row,col,i['author_name'], txt)

                if data['genre_id'] == False:
                    col+=1
                    sheet.write(row,col,i['genre_name'], txt)
                #
                if data['checkout_date'] == False:
                    col+=1
                    sheet.write_datetime(row,col,i['checkout_dte'], date_format)
                #
                if data['return_date'] == False:
                    col+=1
                    sheet.write_datetime(row,col,i['return_dte'], date_format)
                col=3
                row+=1
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()