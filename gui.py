from flask import Flask, render_template, request
from DONTTOUCHME import token
import mysql.connector

cnx = mysql.connector.connect(user='', password='',
                              host='localhost',
                              database='')
cursor = cnx.cursor()

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def main_method():
    #cursor.execute(insertqueryhere)

    return render_template("climbing.html")