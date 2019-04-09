from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import config
import mysql.connector

app = Flask(__name__)
Bootstrap(app)

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
    if style !=  "not applicable":
        where_clause.append("type_name = %(style)s")
        params['style'] = style

    sql = '{} WHERE {}'.format(query, ' AND '.join(where_clause)) + " order by grade"
    return sql, params

@app.route('/', methods=['GET'])
def getClimbs():
    return render_template("mountainproject.html")

@app.route('/', methods=['POST'])
def queryClimbs():


    #return render_template("climbing.html")
    name = request.form.get("climb_name_input")

    style = request.form.get("style_select")

    min_rating = request.form.get("min_rating")
    max_rating = request.form.get("max_rating")

    min_grade = request.form.get("min_grade")
    max_grade = request.form.get("max_grade")

    height = request.form.get("height")
    query, params = getClimbsQuery(name, style, min_grade, max_grade, min_rating, max_rating)
    cursor.execute(query, params)
    rows = cursor.fetchall()

    climb_arr = []
    for row in rows:
        climb = {}
        climb['name'] = row[2]
        climb['description'] = row[3]
        climb['grade'] = row[6]
        climb['rating'] = row[7]
        climb['sandbag'] = row[10]
        climb['style'] = row[11]
        climb_arr.append(climb)

    return render_template("mountainproject.html", climbs = climb_arr)

if __name__ == "__main__":
    app.run()