import os
from dotenv import load_dotenv
import psycopg2
from flask import Flask, render_template

load_dotenv()

app = Flask(__name__)


def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='transactions',
                            user=os.environ['DB_USERNAME'],
                            password=os.environ['DB_PASSWORD'])
    return conn
