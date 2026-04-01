{
    'name': 'Restrict Vendor',
    'depends': ['base','purchase'],
    'data':[
        'views/res_partner_view.xml',
        'views/purchase_order_view.xml',
    ],
    'application': True,
}