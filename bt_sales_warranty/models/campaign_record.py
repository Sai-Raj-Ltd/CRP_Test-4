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
##############################################################################from odoo import api, fields, models, _

from odoo import api, fields, models, _
from datetime import datetime,timedelta,time

class Campaign(models.Model):
    _name = "campaign.details"
    _description = "Campaign Record"
    _inherit = ['mail.thread']
    _rec_name = 'warranty_id' 
    
    warranty_id = fields.Many2one('warranty.details',string='Warranty')
    customer_id = fields.Many2one('res.partner',string='Customer',related='warranty_id.customer_id')
    capture_date = fields.Date(string='Capture Date',track_visibility='onchange')
    campaign_note = fields.Text(string='Note')

# vim:expandtab:smartindent:tabstop=2:softtabstop=2:shiftwidth=2: