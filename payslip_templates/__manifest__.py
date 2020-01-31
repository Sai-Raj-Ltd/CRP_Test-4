# -*- coding: utf-8 -*-
{
    'name': "Professional Payslip Templates",
    'license': 'OPL-1',
    'support': 'support@optima.co.ke',

    'summary': """
        Professional Payslip Templates""",

    'description': """
        Professional Payslip Templates
    """,

    'author': "Optima ICT Services LTD",
    'website': "http://www.optima.co.ke",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Human Resources',
    'version': '0.2',
    'price': 49,
    'currency': 'EUR',
    'images': ['static/description/main.png'],

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr', 'hr_payroll'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'report/payslip.xml',
        'views/company_address.xml',
        'views/company_footer.xml',
        'views/payslip_data.xml',
        'views/payslip_detailed_data.xml',
        'views/switch_template.xml',
        'views/report_detailed_template1.xml',
        'views/report_detailed_template2.xml',
        'views/report_detailed_template3.xml',
        'views/report_detailed_template4.xml',
        'views/report_template1.xml',
        'views/report_template2.xml',
        'views/report_template3.xml',
        'views/report_template4.xml',
        'views/res_config_view.xml',
        'views/payslip_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,

}
