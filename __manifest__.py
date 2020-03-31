# -*- coding: utf-8 -*-
{
    'name': "Pet Klinik",

    'summary': """
       Klinik Pet""",

    'description': """
        Long description of module's purpose
    """,

    'author': "jangakniat",
    'website': "http://www.ubig.co.id",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/client.xml',
        'views/pet.xml',
        'views/appointment.xml',
        'views/doctor.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
