import os
from dotenv import load_dotenv
import psycopg2
from flask import Flask, render_template, request

load_dotenv()

app = Flask(__name__)


def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='transactions',
                            user=os.environ['DB_USERNAME'],
                            password=os.environ['DB_PASSWORD'])
    return conn


# Add a transaction
@app.route("/add", methods=['POST'])
def add_transaction():

    data = request.get_json()

    # Get connection and create curosor
    conn = get_db_connection()
    cur = conn.cursor()

    # Insert transaction data into database
    cur.execute('INSERT INTO transactions (date, vendor, category, amount, notes)'
                'VALUES (%s, %s, %s, %s, %s)',
                (data['date'],
                 data['vendor'],
                 data['category'],
                 data['amount'],
                 data['notes']))
    conn.commit()

    # Close cursor and connection with database
    cur.close()
    conn.close()

    return 'Transaction recorded', 200


if __name__ == "__main__":

    app.run(debug=True)
