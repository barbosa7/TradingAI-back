from flask import Flask,request,redirect,url_for
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

standings = []
btc_price = 0
btc_balance = 0
usdt_balance = 0

@app.route('/',methods = ['POST','GET'])
def show_info():
    if request.method == 'POST':
        data = request.form['info']
        btc_price = request.form['btc_price']
        btc_balance = request.form['btc_balance']
        usdt_balance = request.form['usdt_balance']

        print('we just got some data')
        standings.append(data)
        print(data)
        return standings
    else:
        return standings

@app.route('/basic-info',methods = ['POST','GET'])
def show_info():
    return [btc_price,btc_balance,usdt_balance]
