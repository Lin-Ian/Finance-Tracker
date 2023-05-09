import os
from dotenv import load_dotenv
import psycopg2
from flask import Flask, render_template, request, redirect, url_for
import datetime

load_dotenv()

app = Flask(__name__)


def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='finance_tracker',
                            user=os.environ['DB_USERNAME'],
                            password=os.environ['DB_PASSWORD'])
    return conn


@app.route("/")
def home():
    # Get connection and create cursor
    conn = get_db_connection()
    cur = conn.cursor()

    # Get the subcategories from the expenses table
    cur.execute('SELECT subcategory FROM expenses')
    expense_categories = cur.fetchall()

    # Get the subcategories from the income table
    cur.execute('SELECT subcategory FROM income')
    income_categories = cur.fetchall()

    # Combine categories from both tables
    categories = expense_categories + income_categories

    # Close cursor and connection with database
    cur.close()
    conn.close()

    return render_template('home.html', categories=categories)


@app.route("/view", methods=['GET', 'POST'])
def view():

    try:
        sort_by = request.form['sort_by']
    except:
        sort_by = 'id_inc'
        print("No value given to sort_by")

    # Get connection and create cursor
    conn = get_db_connection()
    cur = conn.cursor()

    # Sort transactions from database
    cur.execute('SELECT * FROM transactions ORDER BY %s' %
                {'id_inc': 'id ASC', 'date_desc': 'date DESC', 'date_inc': 'date ASC',
                 'amount_desc': 'amount DESC', 'amount_inc': 'amount ASC'}[sort_by])
    data = cur.fetchall()

    # Get the subcategories from the expenses table
    cur.execute('SELECT subcategory FROM expenses')
    expense_categories = cur.fetchall()

    # Get the subcategories from the income table
    cur.execute('SELECT subcategory FROM income')
    income_categories = cur.fetchall()

    # Combine categories from both tables
    categories = expense_categories + income_categories

    # Close cursor and connection with database
    cur.close()
    conn.close()

    return render_template('view.html', data=data, categories=categories)


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


# Sort transactions
@app.route("/sort", methods=['GET', 'POST'])
def sort_transactions():

    sort_by = request.form['sort_by']

    # Get connection and create cursor
    conn = get_db_connection()
    cur = conn.cursor()

    # Sort transactions from database
    cur.execute('SELECT * FROM transactions ORDER BY %s' %
                {'date_desc': 'date DESC', 'date_inc': 'date ASC',
                 'amount_desc': 'amount DESC', 'amount_inc': 'amount ASC'}[sort_by])
    data = cur.fetchall()

    # Close cursor and connection with database
    cur.close()
    conn.close()

    return render_template('view.html', data=data)
    # return redirect(url_for('home'))


if __name__ == "__main__":

    app.run(debug=True)
