from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import config
import mysql.connector

app = Flask(__name__)
Bootstrap(app)

cnx = mysql.connector.connect(user=config.USER, password=config.PASSWORD,
                              host=config.HOST,
                              database=config.DATABASE,
                              auth_plugin='mysql_native_password')
cursor = cnx.cursor()

def getClimbsQuery(name="", style="not applicable", min_grade=1, max_grade=13, min_rating=1, max_rating=4, height=""):
    query = "Select climb_name, climb_description, beta, grade, avg_quality_rating, (grade - avg_sugg_grade), group_concat(type_name) " \
            "from climb " \
            "left join climb_type using(climb_id) " \
            "left join type using(type_id) " \
            "left join (select climb_id, AVG(suggested_grade) as avg_sugg_grade " \
            "from suggested_grade " \
            "group by climb_id) as sugg_grade_by_climb using (climb_id) "


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

    if name is not "" and not name.isspace():
        where_clause.append("climb_name like %(name)s")
        params['name'] = '%'+name+'%'
    if style !=  "not applicable":
        where_clause.append("type_name = %(style)s")
        params['style'] = style

    sql = '{} WHERE {}'.format(query, ' AND '.join(where_clause));

    if height is not "":
        sql = sql + " group by climb_id " \
                    "having (select count(*) " \
                    "from user_climb as height_climbs " \
                    "left join user using(user_id) " \
                    "where height_climbs.climb_id = climb_id and " \
                    "user_height >= " + str(height-5) + " and user_height <= " + str(height+5) + ") > 1"
    else:
        sql = sql + " group by climb_id"
    sql = sql + " order by avg_quality_rating desc"
    print(sql)
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
        climb['name'] = row[0]
        climb['description'] = row[1]
        climb['beta'] = row[2]
        climb['grade'] = "V" + str(row[3])
        climb['rating'] = row[4]

        gradeDif = row[5]
        if gradeDif is None:
            gradeDif = "No Suggested Ratings"
        elif gradeDif >= .5:
            gradeDif = "Soft"
        elif gradeDif <= -.5:
            gradeDif = "Sandbagged"
        else:
            gradeDif = "Accurate"

        climb['grade_accuracy'] = gradeDif
        climb['style'] = row[6]
        climb_arr.append(climb)

    return render_template("mountainproject.html", climbs = climb_arr)

if __name__ == "__main__":
    app.run()
