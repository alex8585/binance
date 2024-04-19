#!/usr/bin/python3
import ccxt
import requests
import sys
import time
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('API_KEY')
api_secret = os.getenv('API_SECRET')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

conditions = [
    {'pair':'BTC/USDT', 'price':41600, 'direction': '<'},
    {'pair':'BTC/USDT', 'price':43800, 'direction': '>'},
    # {'pair':'LTC/USDT', 'price':66.21, 'direction': '<'},
    # {'pair':'NEAR/USDT', 'price':2.944, 'direction': '<'},
    # {'pair':'APT/USDT', 'price':8.5, 'direction': '>'},
    # {'pair':'OP/USDT', 'price':3.113, 'direction': '<'},
    # {'pair':'DOGE/USDT', 'price':0.088, 'direction': '>'},
    {'pair':'AVAX/USDT', 'price':36.8, 'direction': '>'},
    {'pair':'AVAX/USDT', 'price':34, 'direction': '<'},
]

def send_tg(message):
    TOKEN = TELEGRAM_TOKEN
    chat_id = TELEGRAM_CHAT_ID
    apiURL = f'https://api.telegram.org/bot{TOKEN}/sendMessage'

    try:
        response = requests.post(apiURL, json={'chat_id': chat_id, 'text': message})
        print(response.text)
    except Exception as e:
        print(e)


def main():
    binance   = ccxt.binance()
    while True: 
        tickers = binance.fetch_tickers()
        # print(tickers['LTC/BTC'])
        for ticker in tickers.values():
            symbol = ticker['symbol'] 
            price = ticker['ask']
            for condition in conditions:
                if condition['pair'] ==  symbol:
                    if (condition['direction'] == '>' and float(price) > float(condition['price'])):
                        send_tg(f'{symbol}  {price}')
                        print('1')
                        return
                    if (condition['direction'] == '<' and float(price) < float(condition['price'])):
                        send_tg(f'{symbol}  {price}')
                        print(price, condition['price'])
                        return

        time.sleep(5)




    # print(binance.fetch_tickers())
if __name__ == "__main__":
   main()
