import os
from dotenv import load_dotenv
import psycopg2
from flask import Flask, render_template, request, redirect, url_for
import datetime
import pandas as pd
import matplotlib.pyplot as plt

load_dotenv()

app = Flask(__name__)


def get_db_connection():
    conn = psycopg2.connect(host=os.environ['DB_HOST'],
                            database=os.environ['DB_NAME'],
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
    except (KeyError, ValueError):
        start_date = None
        end_date = None

    try:
        category = request.form['category']
        if category == 'Category':
            category = ""
    except KeyError:
        category = None

    try:
        vendor = request.form['vendor']
        if vendor == '':
            vendor = None
    except KeyError:
        vendor = None

    try:
        min_amount = request.form['min_amount']
        if min_amount == '':
            min_amount = None
        min_amount = float(min_amount)
    except (KeyError, TypeError):
        min_amount = None

    try:
        max_amount = request.form['max_amount']
        if max_amount == '':
            max_amount = None
        max_amount = float(max_amount)
    except (KeyError, TypeError):
        max_amount = None

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

    if vendor is not None:
        data_df = data_df[data_df['vendor'] == vendor]

    if min_amount is not None and max_amount is not None:
        data_df = data_df[(data_df['amount'] > min_amount) & (data_df['amount'] < max_amount)]

    if min_amount is None and max_amount is not None:
        data_df = data_df[data_df['amount'] < max_amount]

    if min_amount is not None and max_amount is None:
        data_df = data_df[data_df['amount'] > min_amount]

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

    try:
        date = request.form['date']
        date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    except (KeyError, ValueError):
        date = datetime.date.today()

    vendor = request.form['vendor']

    try:
        category = request.form['category']
    except KeyError:
        category = ''

    amount = request.form['amount']

    note = request.form['note']

    missing_fields = False

    if vendor == '' or vendor == '' or amount == '':
        missing_fields = True

    if not missing_fields:
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

    try:
        date = request.form['date']
        date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError:
        date = ''

    vendor = request.form['vendor']
    category = request.form['category']
    amount = request.form['amount']
    note = request.form['note']
    row_id = request.form['id']

    missing_fields = False
    if date == '' or vendor == '' or amount == '':
        missing_fields = True

    if not missing_fields:
        # Get connection and create curosor
        conn = get_db_connection()
        cur = conn.cursor()

        # Edit transaction in database
        cur.execute('UPDATE transactions SET date = %s, vendor = %s, category = %s, amount = %s, notes = %s'
                    'WHERE id = %s', (date, vendor, category, amount, note, row_id))
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
    except (KeyError, FileNotFoundError):
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


@app.route("/insights")
def insights():
    # Get connection and create cursor
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('SELECT SUM(transactions.amount) FROM transactions '
                'JOIN expenses ON transactions.category=expenses.subcategory')
    total_expenses = cur.fetchall()

    cur.execute('SELECT SUM(transactions.amount) FROM transactions '
                'JOIN income ON transactions.category=income.subcategory')
    total_income = cur.fetchall()

    total_expenses = total_expenses[0][0]
    total_income = total_income[0][0]
    net_income = total_income - total_expenses

    pie_labels = ['Income', 'Expenses']
    plt.pie([total_income, total_expenses], labels=pie_labels, startangle=90, autopct='%1.2f%%', counterclock=False)
    plt.title("Income and Expenses")
    plt.savefig('static/images/pie_chart.png')

    cur.execute('SELECT date, amount FROM transactions JOIN expenses ON transactions.category=expenses.subcategory')
    expenses = cur.fetchall()

    expenses = pd.DataFrame(expenses)
    expenses.columns = [x[0] for x in cur.description]
    expenses['date'] = pd.to_datetime(expenses['date'])
    expenses['date'] = expenses['date'].dt.month.astype('int')
    expenses = expenses.groupby('date').sum()
    expenses = expenses.reindex(range(1, 13))
    expenses = expenses.reset_index()
    expenses = expenses.fillna(0)

    cur.execute('SELECT date, amount FROM transactions JOIN income ON transactions.category=income.subcategory')
    income = cur.fetchall()

    income = pd.DataFrame(income)
    income.columns = [x[0] for x in cur.description]
    income['date'] = pd.to_datetime(income['date'])
    income['date'] = income['date'].dt.month.astype('int')
    income = income.groupby('date').sum()
    income = income.reindex(range(1, 13))
    income = income.reset_index()
    income = income.fillna(0)

    net_income_df = income['amount'] - expenses['amount']

    fig = plt.figure()
    plt.bar(income['date'], income['amount'], label='Income')
    plt.bar(expenses['date'], -expenses['amount'], label='Expenses')
    plt.plot(income['date'], net_income_df, label='Net Income', color='green')
    plt.legend()
    plt.title('Income and Expenses Over Time')
    plt.xlabel('Month')
    plt.ylabel('Amount')
    plt.xticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    plt.savefig('static/images/bar_chart.png')

    # Close cursor and connection with database
    cur.close()
    conn.close()

    return render_template("insights.html", total_income=total_income, total_expenses=total_expenses,
                           net_income=net_income)


if __name__ == "__main__":

    app.run(debug=True)
