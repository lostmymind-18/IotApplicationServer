import mysql.connector
import random
import time

cnx = mysql.connector.connect(user='root', password='12345678',
                              host='localhost',
                              database='IotServer')
cursor = cnx.cursor()
i = 0
while i < 100:
	temp = round(random.uniform(18, 40), 2)
	humid = round(random.uniform(30, 90), 2)
	gas = round(random.uniform(15,50),2)
 
	add_data = ("INSERT INTO info "
              "(temp,humid,gas) "
              "VALUES (%s, %s, %s)")
	data = (temp,humid,gas)
	cursor.execute(add_data,data)
	cnx.commit()
	time.sleep(1)
	i+=1

cursor.close()
cnx.close()
 
	
	
