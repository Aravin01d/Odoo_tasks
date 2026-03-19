import json
from odoo import http
from odoo.http import content_disposition, request
from odoo.tools import html_escape

class XLSXReportController(http.Controller):
    @http.route('/xlsx_reports', type='http', auth='user', csrf=False)

    def get_report_xlsx(self, model, options, output_format, report_name, token='ads'):
        """ Return data to python file passed from the javascript"""
        print("You Reached controller")
        session_unique_id = request.session.uid
        report_obj = request.env[model].with_user(session_unique_id)
        options = json.loads(options)
        try:
            if output_format == 'xlsx':
                print("YES XLSX")
                response = request.make_response(
                    None,
                    headers=[('Content-Type', 'application/vnd.ms-excel'),(
                        'Content-Disposition',
                         content_disposition(f"{report_name}.xlsx"))
                    ])
                print("Response:",response)
                report_obj.get_xlsx_report(options, response)
                response.set_cookie('fileToken', token)
                print("Response: ",response)
                return response
        except Exception:
            error = {
                'code': 200,
                'message': 'Odoo Server Error',
            }
            print("Error happened")
            return request.make_response(html_escape(json.dumps(error)))
