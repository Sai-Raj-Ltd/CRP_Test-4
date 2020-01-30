# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Releiver Signing',
    'version' : '1.1',
    'summary': 'Releiver Signing',
    'sequence': 15,
    'description': """Releiver Signing""",
    'category': 'Releiver Signing Management',
    'website': '',
    'depends' : ['base', 'hr_holidays'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
