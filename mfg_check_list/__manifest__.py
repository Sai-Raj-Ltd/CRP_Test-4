
{
    'name': 'SEA Manufacturing Work Order Check List',
    'version': '11.0.1.0.0',
    'summary': """Checklist for Work Order Completion""",
    'description': """Evaluate Work Order completion on the basis of checklists""",
    'category': 'mrp',
    'author': 'Sailotech Pvt Ltd',
    'company': 'Sailotech Pvt Ltd',
    
    'website': "sailotech.com",
    'depends': ['mrp'],
    'data': [
        'security/ir.model.access.csv',
        'views/mrp_checklist_view.xml',
        'views/mfg_checklist_view.xml',
        'views/check_list_view.xml',
        'views/extended_view.xml',
        'views/res_config_settings_views.xml',

        'sql.sql',
    ],
    # 'demo': [
    #     'demo/checklist_demo.xml'
    # ],
    #'images': ['static/description/banner.jpg'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
