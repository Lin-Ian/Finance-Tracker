import os
from dotenv import load_dotenv
import psycopg2

# Load .env file variables
load_dotenv()

# Connect to database
conn = psycopg2.connect(
        host="localhost",
        database="finance_tracker",
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD'])

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
cur.execute('DROP TABLE IF EXISTS transactions;')
cur.execute('CREATE TABLE transactions (id serial PRIMARY KEY,'
                                        'date date NOT NULL,'
                                        'vendor varchar (50) NOT NULL,'
                                        'category varchar (50) NOT NULL,'
                                        'amount decimal NOT NULL,'
                                        'notes varchar (100));'
            )

# Insert data into the table
cur.execute('INSERT INTO transactions (date, vendor, category, amount, notes)'
            'VALUES (%s, %s, %s, %s, %s)',
            ('2023-03-20',
             'Valu-Mart',
             'Groceries',
             10.98,
             '')
            )

cur.execute('INSERT INTO transactions (date, vendor, category, amount, notes)'
            'VALUES (%s, %s, %s, %s, %s)',
            ('2023-01-09',
             'University of Waterloo',
             'Tuition',
             5000,
             '')
            )

# Execute a command: this creates a new table
cur.execute('DROP TABLE IF EXISTS income;')
cur.execute('CREATE TABLE income (subcategory varchar (50) NOT NULL,'
                                  'category varchar (50) NOT NULL);'
            )

income_data = [
    ('Paycheck', 'Earned Income'),
    ('Bonus', 'Earned Income'),
    ('Capital Gains', 'Investment Income'),
    ('Dividends', 'Investment Income'),
    ('Interest Income', 'Investment Income'),
    ('Rental Income', 'Investment Income'),
    ('Tax Refund',	'Tax Refund'),
    ('Grant', 'Financial Aid'),
    ('Scholarship', 'Financial Aid'),
    ('Loan', 'Financial Aid'),
    ('RESP Income', 'Financial Aid'),
    ('Government Benefit', 'Government Benefit'),
    ('Returned Purchase', 'Miscellaneous Income'),
    ('Miscellaneous Income', 'Miscellaneous Income')
]

# cursor.mogrify() to insert multiple values
args = ','.join(cur.mogrify("(%s, %s)", i).decode('utf-8') for i in income_data)

# Insert data into the table
cur.execute('INSERT INTO income (subcategory, category) VALUES ' + args)

# Execute a command: this creates a new table
cur.execute('DROP TABLE IF EXISTS expenses;')
cur.execute('CREATE TABLE expenses (subcategory varchar (50) NOT NULL,'
                                    'category varchar (50) NOT NULL);'
            )

expense_data = [
    ('Mortgage Payment/Rent', 'Housing'),
    ('Property Taxes', 'Housing'),
    ('Maintenance Fees', 'Housing'),
    ('Housing Miscellaneous', 'Housing'),
    ('Gas & Fuel', 'Transportation'),
    ('Parking', 'Transportation'),
    ('Service & Auto Parts', 'Transportation'),
    ('Auto Payment', 'Transportation'),
    ('Auto Insurance', 'Transportation'),
    ('Public Transit', 'Transportation'),
    ('Transportation Miscellaneous', 'Transportation'),
    ('Groceries', 'Food'),
    ('Dining Out', 'Food'),
    ('Alcohol', 'Food'),
    ('Food Misc', 'Food'),
    ('Utilities', 'Utilties'),
    ('Water', 'Utilties'),
    ('Gas', 'Utilties'),
    ('Electricity', 'Utilties'),
    ('Utilties Misc', 'Utilties'),
    ('Television', 'Bills'),
    ('Home Phone', 'Bills'),
    ('Internet', 'Bills'),
    ('Mobile Phone', 'Bills'),
    ('Bills Miscellaneous', 'Bills'),
    ('Insurance', 'Insurance'),
    ('Doctor', 'Health'),
    ('Dentist', 'Health'),
    ('Pharmacy', 'Health'),
    ('Physiotherapy', 'Health'),
    ('Optometry', 'Health'),
    ('Heath Miscellaneous', 'Health'),
    ('Saving', 'Investment'),
    ('TFSA', 'Investment'),
    ('RRSP', 'Investment'),
    ('Non - registered', 'Investment'),
    ('Emergency Fund', 'Investment'),
    ('Debt Repayment', 'Investment'),
    ('Invest Miscellaneous', 'Investment'),
    ('Clothing', 'Personal'),
    ('Home Decore and Furniture', 'Personal'),
    ('Fitness', 'Personal'),
    ('Personal Miscellaneous', 'Personal'),
    ('Subscriptions', 'Entertainment'),
    ('Entertainment Miscellaneous', 'Entertainment'),
    ('Tuition', 'Education'),
    ('Student Fees', 'Education'),
    ('Books & Supplies', 'Education'),
    ('Donations', 'Donations'),
    ('Federal Tax', 'Taxes'),
    ('Provincial Tax', 'Taxes'),
    ('Finance Fees', 'Miscellaneous'),
    ('Miscellaneous', 'Miscellaneous')
]

# cursor.mogrify() to insert multiple values
args = ','.join(cur.mogrify("(%s, %s)", i).decode('utf-8') for i in expense_data)

# Insert data into the table
cur.execute('INSERT INTO expenses (subcategory, category) VALUES ' + args)

conn.commit()

cur.close()
conn.close()
