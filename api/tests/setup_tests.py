from unittest_parametrize import param, parametrize


# Setup data

setup_data = [
    {
        'reference': '000051',
        'date': '2020-01-03',
        'amount': '-51.13',
        'type': 'outflow',
        'category': 'groceries',
        'user_email': 'janedoe@email.com',
    },
    {
        'reference': '000052',
        'date': '2020-01-10',
        'amount': '2500.72',
        'type': 'inflow',
        'category': 'salary',
        'user_email': 'janedoe@email.com',
    },
    {
        'reference': '000053',
        'date': '2020-01-10',
        'amount': '-150.72',
        'type': 'outflow',
        'category': 'transfer',
        'user_email': 'janedoe@email.com',
    },
    {
        'reference': '000054',
        'date': '2020-01-13',
        'amount': '-560.00',
        'type': 'outflow',
        'category': 'rent',
        'user_email': 'janedoe@email.com',
    },
    {
        'reference': '000051',
        'date': '2020-01-04',
        'amount': '-51.13',
        'type': 'outflow',
        'category': 'other',
        'user_email': 'johndoe@email.com',
    },
    {
        'reference': '000689',
        'date': '2020-01-10',
        'amount': '150.72',
        'type': 'inflow',
        'category': 'savings',
        'user_email': 'janedoe@email.com',
    },
]

# Test cases parameters

test_transaction_summary_parameters = parametrize(
    'expected_data',
    [
        param(
            [
                {
                    'user_email': 'janedoe@email.com',
                    'total_inflow': '2651.44',
                    'total_outflow': '-761.85',
                },
                {
                    'user_email': 'johndoe@email.com',
                    'total_inflow': '0.00',
                    'total_outflow': '-51.13',
                },
            ],
            id='all',
        )
    ],
)


test_transaction_summary_by_category_parameters = parametrize(
    'user_email,expected_data',
    [
        param(
            'janedoe@email.com',
            {
                'inflow': {
                    'salary': '2500.72',
                    'savings': '150.72',
                },
                'outflow': {
                    'groceries': '-51.13',
                    'rent': '-560.00',
                    'transfer': '-150.72',
                },
            },
            id='janedoe_transaction_summary_by_category',
        ),
        param(
            'johndoe@email.com',
            {
                'inflow': {},
                'outflow': {
                    'other': '-51.13',
                },
            },
            id='johndoe_transaction_summary_by_category',
        ),
    ],
)
