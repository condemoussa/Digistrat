from odoo import http
from odoo.http import request


class RequeteController(http.Controller):
    @http.route('/Digistrat/dashboard', type='http', auth='user')
    def custom_dashboard(self, **kwargs):
        table1_data = request.env['atm.axe'].search([])
        table2_data = request.env['atm.effet'].search([])

        return request.render('Digistrat.dashboard_template', {
            'table1_data': table1_data,
            'table2_data': table2_data,
        })
