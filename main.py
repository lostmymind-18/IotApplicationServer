from multiprocessing import Manager
from flask import Flask,render_template, request
from flask_mysqldb import MySQL
import time
import datetime
#from flask_script import Manager

 
app = Flask(__name__)
#manager = Manager(app)
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'IotServer'
 
mysql = MySQL(app)
 
@app.route('/form')
def form():
    return render_template('form.html')
 
@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'GET':
        return "Login via the login Form"
     
    if request.method == 'POST':
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        cursor = mysql.connection.cursor()
        cursor.execute(''' INSERT INTO info (time,temp,humid,gas) VALUES(%s,%s,%s,%s)''',(timestamp,34.545,234.53,123.4))
        mysql.connection.commit()
        cursor.close()
        return f"Done!!"
if __name__=='__main__': 
    app.run(host='localhost', port=5000)