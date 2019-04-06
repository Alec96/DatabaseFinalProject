from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import config
import mysql.connector

app = Flask(__name__)

cnx = mysql.connector.connect(user=config.USER, password=config.PASSWORD,
                              host=config.HOST,
                              database=config.DATABASE)
cursor = cnx.cursor()

def getClimbsQuery(name=None, style=None, min_grade=None, max_grade=None, min_rating=None, max_rating=None):
    query = "Select * from climb " \
            "left join climb_type using(climb_id)" \
            "left join type using(type_id)"
    where_clause = []
    params = {}

    where_clause.append("grade >= %(min_grade)s")
    where_clause.append("grade <= %(max_grade)s")
    where_clause.append("avg_quality_rating >= %(min_rating)s")
    where_clause.append("avg_quality_rating <= %(max_rating)s")
    params['min_grade'] = min_grade
    params['max_grade'] = max_grade
    params['min_rating'] = min_rating
    params['max_rating'] = max_rating

    if name is not "":
        where_clause.append("climb_name = %(name)s")
        params['name'] = name
    if style is not None:
        where_clause.append("type = %(style)s")
        params['style'] = style

    sql = '{} WHERE {}'.format(query, ' AND '.join(where_clause))
    return sql, params

@app.route('/', methods=['GET'])
def getClimbs():
    return render_template("mountainproject.html")

@app.route('/', methods=['POST'])
def queryClimbs():


    #return render_template("climbing.html")
    name = request.form.get("climb_name")

    style = request.form.get("style_select")

    min_rating = request.form.get("min_rating")
    max_rating = request.form.get("min_rating")

    min_grade = request.form.get("min_grade")
    max_grade = request.form.get("max_grade")

    height = request.form.get("height")
    if min_grade == "na":
        min_grade = 0
    if max_grade == "na":
        max_grade = 13

    if min_rating == "na":
        min_rating = 0
    if max_rating == "na":
        max_rating = 4

    query, params = getClimbsQuery(name, style, min_grade, max_grade, min_rating, max_rating)
    cursor.execute(query, params)
    rows = cursor.fetchall()


    for row in rows:
        print(row)

    return render_template("mountainproject.html")

if __name__ == "__main__":
    app.run()