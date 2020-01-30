# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2017 BroadTech IT Solutions Pvt Ltd 
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
import datetime

class Warrantyextention(models.TransientModel):
    _name = "warranty.extention"
    _description = "Warranty Extention"
    
    extended_date = fields.Date(string='Warranty Extended Date')
    
    @api.multi
    def warrantyextended(self):
        active_warranty = self.env['warranty.details'].browse(self._context.get('active_ids',[]))
        active_warranty.write({'warranty_end_date':self.extended_date,'state':'inwarranty'})
        active_warranty.message_post(body=_("Warranty Extended"))
        return True 

# vim:expandtab:smartindent:tabstop=2:softtabstop=2:shiftwidth=2: