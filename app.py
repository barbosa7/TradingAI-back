from flask import Flask,request,redirect,url_for
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

standings = []

@app.route('/',methods = ['POST','GET'])
def show_info():
    if request.method == 'POST':
        data = request.form['info']
        print('we just got some data')
        standings.append(data)
        print(data)
        return standings
    else:
        return standings
