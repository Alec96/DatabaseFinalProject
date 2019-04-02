from flask import Flask, render_template, request
app = Flask(__name__)
#import mysql.connector

# cnx = mysql.connector.connect(user='', password='',
#                               host='localhost',
#                               database='')
# cursor = cnx.cursor()


@app.route('/', methods=['GET', 'POST'])
def getClimbs():
    #cursor.execute(insertqueryhere)
    #return render_template("climbing.html")
    return render_template("climbing.html")

if __name__ == "__main__":
    app.run()