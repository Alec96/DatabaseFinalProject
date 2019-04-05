from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import config
app = Flask(__name__)
import mysql.connector

cnx = mysql.connector.connect(user=config.USER, password=config.PASSWORD,
                              host=config.HOST,
                              database=config.DATABASE)
cursor = cnx.cursor()


@app.route('/', methods=['GET'])
def getClimbs():
    #cursor.execute(insertqueryhere)
    #return render_template("climbing.html")
    return render_template("mountainproject.html")

@app.route('/', methods=['POST'])
def queryClimbs():
    query = "Select title from book"
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    #return render_template("climbing.html")
    style = request.form.get("style_select")

    min_rating = request.form.get("min_rating")
    max_rating = request.form.get("min_rating")

    min_grade = request.form.get("min_grade")
    max_grade = request.form.get("max_grade")

    height = request.form.get("height")
    return render_template("mountainproject.html")

if __name__ == "__main__":
    app.run()