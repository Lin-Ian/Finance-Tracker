import os
from dotenv import load_dotenv
import psycopg2
from flask import Flask, render_template, request, redirect, url_for
import datetime

load_dotenv()

app = Flask(__name__)


def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='transactions',
                            user=os.environ['DB_USERNAME'],
                            password=os.environ['DB_PASSWORD'])
    return conn


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/view")
def view():
    # Get connection and create cursor
    conn = get_db_connection()
    cur = conn.cursor()

    # Insert transaction data into database
    cur.execute('SELECT * FROM transactions')
    data = cur.fetchall()

    # Close cursor and connection with database
    cur.close()
    conn.close()

    return render_template('view.html', data=data)


# Add a transaction
@app.route("/add", methods=['POST'])
def add_transaction():

    date = request.form['date']
    date = datetime.datetime.strptime(date, '%Y-%m-%d').date()

    vendor = request.form['vendor']
    category = request.form['category']
    amount = request.form['amount']
    print(type(amount))
    note = request.form['note']

    # Get connection and create cursor
    conn = get_db_connection()
    cur = conn.cursor()

    # Insert transaction data into database
    cur.execute('INSERT INTO transactions (date, vendor, category, amount, notes)'
                'VALUES (%s, %s, %s, %s, %s)',
                (date, vendor, category, amount, note))
    conn.commit()

    # Close cursor and connection with database
    cur.close()
    conn.close()

    # return 'Transaction recorded', 200
    return redirect(url_for('home'))


# Edit a transaction
@app.route("/update", methods=['POST'])
def edit_transaction():

    date = request.form['date']
    date = datetime.datetime.strptime(date, '%Y-%m-%d').date()

    vendor = request.form['vendor']
    category = request.form['category']
    amount = request.form['amount']
    note = request.form['note']
    row_id = request.form['id']

    # Get connection and create curosor
    conn = get_db_connection()
    cur = conn.cursor()

    # Edit transaction in database
    cur.execute('UPDATE transactions SET date = %s, vendor = %s, category = %s, amount = %s, notes = %s WHERE id = %s',
                (date, vendor, category, amount, note, row_id))
    conn.commit()

    # Close cursor and connection with database
    cur.close()
    conn.close()

    return redirect(url_for('view'))


# Delete a transaction
@app.route("/delete", methods=['POST'])
def delete_transaction():

    row_id = request.form['id']

    # Get connection and create cursor
    conn = get_db_connection()
    cur = conn.cursor()

    # Delete transaction data from database
    cur.execute('DELETE FROM transactions WHERE id = %s',
                row_id)
    conn.commit()

    # Close cursor and connection with database
    cur.close()
    conn.close()

    return redirect(url_for('view'))


if __name__ == "__main__":

    app.run(debug=True)
