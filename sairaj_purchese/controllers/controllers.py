# -*- coding: utf-8 -*-
from odoo import http

# class SairajPurchese(http.Controller):
#     @http.route('/sairaj_purchese/sairaj_purchese/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sairaj_purchese/sairaj_purchese/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sairaj_purchese.listing', {
#             'root': '/sairaj_purchese/sairaj_purchese',
#             'objects': http.request.env['sairaj_purchese.sairaj_purchese'].search([]),
#         })

#     @http.route('/sairaj_purchese/sairaj_purchese/objects/<model("sairaj_purchese.sairaj_purchese"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sairaj_purchese.object', {
#             'object': obj
#         })