# -*- coding: utf-8 -*-
from odoo import http

# class SairajAccounting(http.Controller):
#     @http.route('/sairaj_accounting/sairaj_accounting/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sairaj_accounting/sairaj_accounting/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sairaj_accounting.listing', {
#             'root': '/sairaj_accounting/sairaj_accounting',
#             'objects': http.request.env['sairaj_accounting.sairaj_accounting'].search([]),
#         })

#     @http.route('/sairaj_accounting/sairaj_accounting/objects/<model("sairaj_accounting.sairaj_accounting"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sairaj_accounting.object', {
#             'object': obj
#         })