# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2017-BroadTech IT Solutions (<http://www.broadtech-innovations.com/>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
##############################################################################

{
    'name': 'Sales Warranty',
    'version': '0.1',
    'author' : 'BroadTech IT Solutions Pvt Ltd',
    'category': 'Sales',
    'license':'AGPL-3',
    'summary' : 'Sales Warranty ',
    'description': """
The module helps to manage the warranty details and service information of products sold to customers and thus smoothen the after sales activities.
    """,
    'website': 'http://www.broadtech-innovations.com',
    'depends': ['sale'],
    'data': [
        'data/warranty_name_sequence.xml',
        'data/warranty_expire_scheduler.xml',
        'security/ir.model.access.csv',
        'wizard/warranty_extention.xml',
        'views/warranty_record_view.xml',
        'views/service_record_view.xml',
        'views/campaign_record_view.xml',
        'report/warranty_report.xml',
        'report/warranty_detail_report.xml'
    ],
    'images': ['static/description/bt_sales_warranty_banner.jpg'],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=2:softtabstop=2:shiftwidth=2:
