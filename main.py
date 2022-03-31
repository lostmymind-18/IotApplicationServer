from multiprocessing import Manager
from flask import Flask,render_template, request
from flask_mysqldb import MySQL
#from flask_script import Manager

 
app = Flask(__name__)
#manager = Manager(app)
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'IotServer'
 
mysql = MySQL(app)
 
@app.route('/', methods = ['GET'])
def login():
    if request.method == 'GET':
        #while True:
            cursor = mysql.connection.cursor()
            cursor.execute(''' SELECT * FROM info ORDER BY time DESC LIMIT 1''')
            result = cursor.fetchall()[0]
            temp = result[1]
            humid = result[2]
            gas = result[3]
            light = result[4]
            mysql.connection.commit()
            cursor.close()
            return render_template('page.html',temp=temp,
                humid=humid,gas=gas,light=light)
if __name__=='__main__': 
    app.run(host='localhost', port=5000)