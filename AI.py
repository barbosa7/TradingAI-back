import json
import threading
import time
from binance import Client
from pprint import pformat
from http import client
from time import sleep
import asyncio
import requests
import os
import pandas as pd
import binance.enums
from binance.exceptions import BinanceAPIException # here
from datetime import datetime
import json, hashlib, hmac, time
from urllib.parse import urljoin, urlencode
import urllib.parse,  urllib.request
import json


quantity = 0.001

DB= pd.read_csv('DB.csv')
#test_api = 'l6syo1EwvJxParRFlqEf7SOH33YpBIEz2J8dGlgZJhWEfsJGBHCII6T60Lf3m55j'
#test_secret = 'Ep6zRq6kTEFzdnd5WPgz8CUUuI4po0J67vOM1XquXjXnohbkwpws0AERRioMu1w4'
apiKey = "OGksfmxblrQHEnf5etbTEOpERqidTIllYyf1dD8C82CFBR5U65KKaE0UhIzUXPrb"
secret = "59rPBrtJjy8j6SEbPUo9deNpM2bTMGKUPL3Jke3Jgr2X8VlwVvfXkqonqKoecYDl"
binance_api = os.environ.get('binance_api')
binance_key = os.environ.get('binance_secret')


client = Client(apiKey, secret)
# # manually set the endpoint to the testnet
print(client.get_asset_balance(asset='USDT'))

btc_price = client.get_symbol_ticker(symbol="BTCUSDT")
print(btc_price)
def change_position(curr,is_buy):
    if is_buy:
        DB.loc[DB.Currency == curr, 'Position'] += 1
    else:
        DB.loc[DB.Currency == curr, 'Position'] -= 1
    DB.to_csv('Position', index=False)

def get_hourly_data(symbol):
    frame = pd.DataFrame(client.get_historical_klines(symbol,Client.KLINE_INTERVAL_1MINUTE,'1 hour ago UTC'))
    frame = frame.iloc[:,:5]
    frame.columns = ['Time','Open','High','Low','Close']
    frame[['Open','High','Low','Close']]=frame[['Open','High','Low','Close']].astype(float)
    frame.Time = pd.to_datetime(frame.Time, unit='ms')
    return frame

        #session = requests.Session()
        #register_url="http:///sapi/v1/margin/order?"
        #response = session.post(f"{register_url}",data={"symbol": 'BTCUSDT',"side": 'BUY',"type": 'LIMIT',"quantity": '0.05',"price": float(round(float(current_price)-20.0,5)),'timeInForce': 'GTC'})
def market_make(asset1,asset2):
    curr = asset1+asset2
    data = client.get_symbol_ticker(symbol=curr)
    current_price=data["price"]
    qty = DB[DB.Currency==curr].Quantity.values[0]
    try:
        if (float(client.get_asset_balance(asset=asset1)['free'])>=quantity):
            sell_order = client.create_order(symbol=curr,side='SELL',type='LIMIT',timeInForce='GTC',quantity=quantity,price=float(round(float(current_price)+20.0,5)))
            print(sell_order)
        if ((float(client.get_asset_balance(asset=asset2)['free'])/float(client.get_symbol_ticker(symbol=curr)['price']))>=quantity):
            buy_order = client.create_order(symbol=curr,side='BUY',type='LIMIT',timeInForce='GTC',quantity=quantity,price=float(round(float(current_price)-20.0,5)))
            print(buy_order)
    except BinanceAPIException as e:
        print(e)

#client.cancel_orders(symbol='BTCUSDT')
#client.cancel_order('BTCUSDT',)

while True:
    market_make('BTC','USDT')
    print(client.get_asset_balance(asset='BTC'))
    print(client.get_asset_balance(asset='USDT'))
    USDT_balance = client.get_asset_balance(asset='USDT')
    btc_balance=float(client.get_asset_balance(asset='BTC')['free']) + float(client.get_asset_balance(asset='BTC')['locked'])
    btc_price = float(client.get_symbol_ticker(symbol="BTCUSDT")['price'])
    total_balance= btc_balance*btc_price + float(USDT_balance['free']) + float(USDT_balance['locked'])
    print("Current Time =",datetime.now())
    print('current balance: ' + str(total_balance))
    standings = (str(datetime.now()).split(' ')[1] + ' ' + str(total_balance))
    requests.post('http://127.0.0.1:5000',data={"info": standings})
    time.sleep(300)
    client = Client(apiKey, secret)
    #client.API_URL = 'https://testnet.binance.vision/api'











# # #Websocket connectionß
# #c = close
# #

# def btc_trade_history(msg):
#     ''' define how to process incoming WebSocket messages 
#     if msg['e'] != 'error':
#         print(msg['c'])
#         btc_price['last'] = msg['c']
#         btc_price['bid'] = msg['b']
#         btc_price['last'] = msg['a']
#         btc_price['error'] = False
#     else:
#         btc_price['error'] = True
# '''
#     print(f"message type: {msg['e']}")
#     print(msg)

# #start the websocket
# bsm = ThreadedWebsocketManager(client)
# bsm.start()
# bsm.start_kline_socket(callback=btc_trade_history, symbol=symbol)
# #bsm.stop()