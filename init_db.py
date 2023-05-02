import os
from dotenv import load_dotenv
import psycopg2

# Load .env file variables
load_dotenv()

# Connect to database
conn = psycopg2.connect(
        host="localhost",
        database="transactions",
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
                                        'amount money NOT NULL,'
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

conn.commit()

cur.close()
conn.close()
