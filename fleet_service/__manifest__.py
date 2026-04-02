{
    'name': 'Fleet Service',
    'depends':['base','fleet','hr'],
    'data':[
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/fleet_service_order_view.xml',
        'views/fleet_vehicle_view.xml',
        'views/hr_employee_view.xml',
        'views/fleet_service_menu.xml',
    ],
    'application':'True',
}