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

def getClimbsQuery(name="", style="not applicable", min_grade=1, max_grade=13, min_rating=1, max_rating=4, height=""):
    query = "Select * from climb as init_climb " \
            "left join climb_type using(climb_id)" \
            "left join type using(type_id)"
    try:
        height =  int(height)
    except:
        height = ""
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

    sql = '{} WHERE {}'.format(query, ' AND '.join(where_clause));

    if height is not "":
        sql = sql + " having (select count(*) from user_climb " \
                    "left join user using(user_id) " \
                    "where climb_id = init_climb.climb_id and " \
                    "user_height >= " + str(height-5) + " and user_height <= " + str(height+5) + ") > 1"
    sql = sql + " order by avg_quality_rating desc"
    return sql, params

@app.route('/', methods=['GET'])
def getClimbs():
    return render_template("mountainproject.html")

@app.route('/', methods=['POST'])
def queryClimbs():

    name = request.form.get("climb_name_input")

    style = request.form.get("style_select")

    min_rating = request.form.get("min_rating")
    max_rating = request.form.get("max_rating")

    min_grade = request.form.get("min_grade")
    max_grade = request.form.get("max_grade")

    height = request.form.get("height")
    query, params = getClimbsQuery(name, style, min_grade, max_grade, min_rating, max_rating, height)
    cursor.execute(query, params)
    rows = cursor.fetchall()

    climb_arr = []
    for row in rows:
        climb = {}
        climb['name'] = row[2]
        climb['description'] = row[3]
        climb['grade'] = "V" + str(row[6])
        climb['rating'] = row[7]
        climb['Grade Accuracy'] = row[10]
        climb['style'] = row[11]
        climb_arr.append(climb)

    return render_template("mountainproject.html", climbs = climb_arr)

if __name__ == "__main__":
    app.run()