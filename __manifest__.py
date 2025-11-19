# -*- coding: utf-8 -*-
###############################################################################
#
#    POS Stock Transfer & Scrap Management
#
###############################################################################

{
    'name': 'Point of Sale Stock Transfer & Scrap Management',
    'version': '17.0.1.0.0',
    'category': 'Point of Sale',
    'summary': "Create Stock Transfers & Scrap Products Directly From POS",
    'description': """
        This module adds two new inventory features inside POS:
        - Stock Transfer button with picking type selection & live transfer creation.
        - Scrap Products button with popup reason & automatic scrap creation.
        Both features work directly inside the POS Product Screen.
    """,
    'author': 'Cybrosys Techno Solutions / Modified by You',
    'website': 'https://www.cybrosys.com',
    'company': 'Cybrosys Techno Solutions',
    'license': 'AGPL-3',

    'depends': [
        'base',
        'point_of_sale',
        'stock',
    ],

    'data': [
        'views/res_config_settings_views.xml',
    ],

    'assets': {
        'point_of_sale._assets_pos': [

            
            '/stock_transfer_in_pos/static/src/xml/stock_transfer_button.xml',
            '/stock_transfer_in_pos/static/src/xml/transfer_create_popup.xml',
            '/stock_transfer_in_pos/static/src/xml/transfer_ref_popup.xml',

           
            '/stock_transfer_in_pos/static/src/js/stock_transfer.js',
            '/stock_transfer_in_pos/static/src/js/transfer_create_popup.js',
            '/stock_transfer_in_pos/static/src/js/transfer_ref_popup.js',

            
            '/stock_transfer_in_pos/static/src/xml/scrap_button.xml',
            '/stock_transfer_in_pos/static/src/xml/scrap_reason_popup.xml',
            '/stock_transfer_in_pos/static/src/xml/scrap_success_popup.xml',
            '/stock_transfer_in_pos/static/src/xml/pos_scrap_orders_screen.xml',

            
            '/stock_transfer_in_pos/static/src/js/scrap_button.js',
            '/stock_transfer_in_pos/static/src/js/scrap_reason_popup.js',
            '/stock_transfer_in_pos/static/src/js/scrap_success_popup.js',
            '/stock_transfer_in_pos/static/src/js/pos_scrap_orders_screen.js',
        ],
    },

    'images': ['static/description/banner.jpg'],

    'installable': True,
    'application': True,
    'auto_install': False,
}
