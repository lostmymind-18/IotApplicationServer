from urllib import response
from flask import Flask,render_template,url_for,request,redirect, make_response
import random
import json
from time import time
from random import random
from flask import Flask, render_template, make_response
from flask_mysqldb import MySQL
app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'IotServer'

mysql = MySQL(app)

@app.route('/', methods=["GET", "POST"])
def main():
    return render_template('index.html')


@app.route('/data', methods=["GET", "POST"])
def data():
    # Data Format
    # [TIME, Temperature, Humidity]

    cursor = mysql.connection.cursor()
    cursor.execute(''' SELECT * FROM info ORDER BY time DESC LIMIT 1''')
    result = cursor.fetchall()[0]
    timee = result[0]
    temp = result[1]
    humid = result[2]
    gas = result[3]
    light = result[4]
    mysql.connection.commit()
    cursor.close()
    data = [time()*1000,temp,humid]
    response = make_response(json.dumps(data,indent=4,sort_keys=True, default=str))
    response.content_type = 'application/json'
    return response


if __name__ == "__main__":
    app.run(debug=True)
