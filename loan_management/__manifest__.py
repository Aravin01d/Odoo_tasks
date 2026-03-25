{
    'name': 'Loan Management',
    'depends':['base','hr'],
    'data':[
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/employee_loan_view.xml',
        'views/employee_loan_line_view.xml',
        'views/loan_menu_view.xml',
    ],
    'application':'True',
}