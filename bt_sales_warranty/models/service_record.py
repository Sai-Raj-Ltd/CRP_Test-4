
# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2018 BroadTech IT Solutions Pvt Ltd 
#    (<http://broadtech-innovations.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import api, fields, models, _
from datetime import datetime,timedelta,time

class Service(models.Model):
    
    _name = "service.details"
    _description = "Service Record"
    _inherit = ['mail.thread']
    _rec_name = 'warranty_id'
     
    warranty_id = fields.Many2one('warranty.details',string='Warranty')
    product_id = fields.Many2one('product.product',string='Product', related='warranty_id.product_id')
    sno = fields.Char(string='Serial No' , related='warranty_id.sno')
    warranty_end_date = fields.Date(related='warranty_id.warranty_end_date')
    date_received = fields.Date(string='Received Date',track_visibility='onchange',default=fields.Date.context_today)
    complaint_note = fields.Text(string='Description',track_visibility='onchange')
    service_note = fields.Text(string='Service Note')
    return_date = fields.Date(string='Date of Return',track_visibility='onchange')
    warranty_expired = fields.Boolean(string = "Warranty Expired", track_visibility='onchange')
    state = fields.Selection([('registered','Registered'),
                              ('inservice','In Service'),
                              ('done','Service Done'),
                              ('delivered','Delivered')], default='registered',string = "Status",track_visibility='onchange')
    
    @api.multi
    def action_state_process(self,vals):
        for service in self:
            service.state = 'inservice'
        
    @api.multi
    def action_state_done(self,vals):
        for service in self:
            service.state = 'done'
        
    @api.multi
    def action_state_deliver(self,vals):
        for service in self:
            service.state = 'delivered'
    
    @api.multi
    def action_state_replace(self,vals):
        for service in self:
            service.warranty_expired = True
            service.state = 'delivered'
            service.warranty_id.state = 'expired'
        
    # vim:expandtab:smartindent:tabstop=2:softtabstop=2:shiftwidth=2:    
                   