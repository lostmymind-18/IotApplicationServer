from urllib import response
from flask import Flask,render_template,url_for,request,redirect, make_response
import random
import json
from time import time
from random import random
from flask import Flask, render_template, make_response
from Adafruit_IO import Client, Feed

ADAFRUIT_IO_KEY = 'aio_omRU24MZwW4FwXEHyzg2wl1MjPxA'

# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username)
ADAFRUIT_IO_USERNAME = 'phmngnlgvu'

# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)


app = Flask(__name__)

def receiveData():
    return (aio.receive('ttdadn.temp').value, aio.receive('ttdadn.humi').value)

@app.route('/', methods=["GET", "POST"])
def main():
    return render_template('index.html')


@app.route('/data', methods=["GET", "POST"])
def data():
    # Data Format
    # [TIME, Temperature, Humidity]

    receive = receiveData()
    data = [time()*1000,int(receive[0]),int(receive[1])]
    response = make_response(json.dumps(data,indent=4,sort_keys=True, default=str))
    response.content_type = 'application/json'
    return response


if __name__ == "__main__":
    app.run(debug=True)