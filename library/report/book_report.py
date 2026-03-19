from odoo import models, api

class BookReport(models.AbstractModel):
    _name = 'report.library.report_book'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs=self.env['book.report.wizard'].browse(docids)
        print("data:",data)
        print("docs:",docs)
        print('docids:', docids)
        return{
            'doc_ids':docids,
            'doc_model':'book.report.wizard',
            'docs':docs,
            'data':data,
        }
