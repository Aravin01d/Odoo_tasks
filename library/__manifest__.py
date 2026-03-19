{
    'name': "Library",
    'depends': ['base','mail','contacts','sale','account','purchase'],
    'category':'library',
    'data':[
        'security/groups.xml',
        'security/ir.model.access.csv',

        'data/sequence.xml',
        'data/demo_data.xml',
        'data/email.xml',

        'report/ir_actions_report.xml',
        'report/report_template.xml',

        'views/books_view.xml',
        'views/authors_view.xml',
        'views/publishers_view.xml',
        'views/checkouts_view.xml',
        'views/genres_view.xml',
        'views/checkoutlines_view.xml',
        'views/res_partner_view.xml',
        'views/purchase_order.xml',
        # 'views/purchase_order_line.xml',
        'views/account_move.xml',
        'views/settings_view.xml',

        'wizard/product_menu_view.xml',
        'wizard/suggest_book_view.xml',
        'wizard/book_report_wizard_view.xml',
        'views/library_menus.xml'
    ],
    'application':'True',
    'assets':{
        'web.assets_backend':[
            'library/static/src/js/action_manager.js'
        ]
    }
}

