# -*- coding: utf-8 -*-
from odoo import http

# class SairajInventory(http.Controller):
#     @http.route('/sairaj_inventory/sairaj_inventory/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sairaj_inventory/sairaj_inventory/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sairaj_inventory.listing', {
#             'root': '/sairaj_inventory/sairaj_inventory',
#             'objects': http.request.env['sairaj_inventory.sairaj_inventory'].search([]),
#         })

#     @http.route('/sairaj_inventory/sairaj_inventory/objects/<model("sairaj_inventory.sairaj_inventory"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sairaj_inventory.object', {
#             'object': obj
#         })