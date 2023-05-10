import os
from dotenv import load_dotenv
import psycopg2
from flask import Flask, render_template, request, redirect, url_for
import datetime
import pandas as pd

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
    except KeyError:
        sort_by = 'default'

    try:
        start_date = request.form['start_date']
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = request.form['end_date']
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
    except KeyError:
        start_date = None
        end_date = None
    except ValueError:
        start_date = None
        end_date = None

    try:
        category = request.form['category']
        if category == 'Category':
            category = ""
    except KeyError:
        category = None

    # Get connection and create cursor
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('SELECT * FROM transactions')
    data_df = pd.DataFrame(cur.fetchall())
    data_df.columns = [x[0] for x in cur.description]

    # Get the transactions within a date range
    if not (start_date is None and end_date is None):
        data_df = data_df[(data_df['date'] >= start_date) & (data_df['date'] <= end_date)]

    if category is not None:
        data_df = data_df[data_df['category'] == category]

    if sort_by != 'default':
        sort_by = {'default': ['id', True], 'date_desc': ['date', False], 'date_inc': ['date', True],
                   'amount_desc': ['amount', False], 'amount_inc': ['amount', True]}[sort_by]
        data_df = data_df.sort_values(by=sort_by[0], ascending=sort_by[1])

    data = data_df.values.tolist()

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
    cur.execute('DELETE FROM transactions WHERE id = %s' % row_id)
    conn.commit()

    # Close cursor and connection with database
    cur.close()
    conn.close()

    return redirect(url_for('view'))


@app.route("/upload", methods=['GET', 'POST'])
def upload_transactions():
    try:
        file = request.files['file']
        filename = file.filename
        file.save(filename)
        message = "Transactions uploaded successfully"
    except KeyError:
        filename = ""
        message = ""

    if filename != "":
        # Read csv file
        data = pd.read_csv(filename)
        data = data.fillna('')

        # Get connection and create cursor
        conn = get_db_connection()
        cur = conn.cursor()

        # Insert data from csv file
        for col, row in data.iterrows():
            values = (row['date'], row['vendor'], row['category'], row['amount'], row['notes'])
            cur.execute('INSERT INTO transactions (date, vendor, category, amount, notes)'
                        'VALUES (%s, %s, %s, %s, %s)', values)
        conn.commit()

        # Close cursor and connection with database
        cur.close()
        conn.close()

        # Remove file after contents uploaded to database
        os.remove(filename)

    return render_template("upload.html", message=message, filename=filename)


if __name__ == "__main__":

    app.run(debug=True)
