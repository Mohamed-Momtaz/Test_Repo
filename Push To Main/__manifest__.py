
{
    'name': 'HR Penalty And Bonus',
    'summary': 'HR Penalty And Bonus',
    'author': "knowledge BI , Mahmoud Elfeky",
    'company': 'knowledge BI',
    'website': "https://www.knowledgebi.net/",
    'version': '15.0.0.1.0',
    'category': 'HR',
    'license': 'AGPL-3',
    'sequence': 1,
    'depends': [
        'base',
        'hr',
        'hr_payroll',
        'hr_customization',
        'hr_work_entry_contract_enterprise',
    ],
    'data': [
        'security/ir.model.access.csv',
        # 'report/',
        # 'wizard/',
        'views/allowance.xml',
        'views/hr_payslip.xml',
        'views/penalty.xml',
    ],
    'demo': [
        # 'demo/',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

