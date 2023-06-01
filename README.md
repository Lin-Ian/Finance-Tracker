# Finance-Tracker

A Flask web application with a PostgreSQL database to track and monitor financial transactions.

## Table of Contents
- [Motivation and Outcomes](#motivation-and-outcomes)
- [Technologies](#technologies)
- [Installation](#installation)
- [Features](#features)
  - [Home](#home)
  - [View](#view)
  - [Upload](#upload)
  - [Insights](#insights)

## Motivation and Outcomes
I wanted to consolidate all my financial transactions into a single place to 

## Technologies
This project is created with:
- Python 3.10
- Flask 2.3.2
- pandas 2.0.1
- matplotlib 3.7.1
- PostgreSQL 15.2

This project is hosted on:

## Installation
1. Clone the repository
```
$ git clone https://github.com/Lin-Ian/Finance-Tracker.git
```
2. Install Requirements
```
pip install -r requirements.txt
```
3. Run
```
py app.py
```
Open the localhost link, and you're ready to start tracking your transactions now

## Features
### Home
- Enter transactions to be stored in database
- Store important data like the date, vendor, category, amount, and any notes about your transaction

<img src="media/home.png" alt="Screenshot of home page" width="500">

### View
- View entered transactions
- Sort by default, date, or amount
- Filter transactions based on date, category, vendor, and/or amount
- Save your (filtered) transactions as a CSV file
- Update or delete any transactions

<img src="media/view.png" alt="Screenshot of view page" width="500">

### Upload
- Upload transactions stored in a CSV file if there are too many to enter one at a time

- <img src="media/upload.png" alt="Screenshot of upload page" width="500">

### Insights
- Gain more insights about your transactions
- See your total income and expenses, net income, and savings rate
- Intuitive visuals to view your income and expenses

<img src="media/insights.png" alt="Screenshot of view page" width="500">
