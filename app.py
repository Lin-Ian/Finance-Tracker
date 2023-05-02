import os
from dotenv import load_dotenv
import psycopg2
from flask import Flask, render_template, request, jsonify

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


# Edit a transaction
@app.route("/edit/<row_id>", methods=['POST'])
def edit_transaction(row_id):

    data = request.get_json()

    # Get connection and create curosor
    conn = get_db_connection()
    cur = conn.cursor()

    # Insert transaction data into database
    cur.execute('UPDATE transactions SET date = %s, vendor = %s, category = %s, amount = %s, notes = %s WHERE id = %s',
                (data['date'],
                 data['vendor'],
                 data['category'],
                 data['amount'],
                 data['notes'],
                 row_id))
    conn.commit()

    # Close cursor and connection with database
    cur.close()
    conn.close()

    return 'Transaction edited', 200


# View all transactions
@app.route("/view", methods=['GET'])
def view_transactions():
    # Get connection and create curosor
    conn = get_db_connection()
    cur = conn.cursor()

    # Get all transaction data from database
    cur.execute('SELECT * FROM transactions')
    data = cur.fetchall()

    # Close cursor and connection with database
    cur.close()
    conn.close()

    return data, 200


# View a transaction
@app.route("/view/<row_id>", methods=['GET'])
def view_transaction(row_id):

    # Get connection and create curosor
    conn = get_db_connection()
    cur = conn.cursor()

    # Insert transaction data into database
    cur.execute('SELECT * FROM transactions WHERE id = %s',
                row_id)
    data = cur.fetchall()

    # Close cursor and connection with database
    cur.close()
    conn.close()

    return data, 200


# Delete a transaction
@app.route("/delete/<row_id>", methods=['DELETE'])
def delete_transaction(row_id):

    # Get connection and create curosor
    conn = get_db_connection()
    cur = conn.cursor()

    # Delete transaction data from database
    cur.execute('DELETE FROM transactions WHERE id = %s',
                row_id)
    conn.commit()

    # Close cursor and connection with database
    cur.close()
    conn.close()

    return "Transaction deleted", 200


if __name__ == "__main__":

    app.run(debug=True)
