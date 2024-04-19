#!/usr/bin/python3
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
import requests
import sys
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('API_KEY')
api_secret = os.getenv('API_SECRET')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
 
conditions = [
    {'pair':'BTCUSDT', 'price':39500, 'direction': '<'},
    {'pair':'BTCUSDT', 'price':41299, 'direction': '>'},
    # {'pair':'LTCUSDT', 'price':66.21, 'direction': '<'},
    # {'pair':'NEARUSDT', 'price':2.944, 'direction': '<'},
    # {'pair':'APTUSDT', 'price':8.39, 'direction': '<'},
    # {'pair':'OPUSDT', 'price':3.113, 'direction': '<'},
    # {'pair':'BONKUSDT', 'price':0.00001150, 'direction': '<'},
    # {'pair':'DOGEUSDT', 'price':0.088, 'direction': '>'},
    # {'pair':'DOGEUSDT', 'price':0.085, 'direction': '<'},
    # {'pair':'ETHUSDT', 'price':2600, 'direction': '>'}
]

# streams = ['btcusdt@trade', 'ethusdt@trade', 'ltcusdt@trade',  'nearusdt@trade',   'aptusdt@trade']
streams = []
for condition in conditions:
   pair = condition['pair'].lower()
   stream = f'{pair}@trade'
   streams.append(stream)


def send_tg(message):
    TOKEN = TELEGRAM_TOKEN 
    chat_id = TELEGRAM_CHAT_ID
    apiURL = f'https://api.telegram.org/bot{TOKEN}/sendMessage'

    try:
        response = requests.post(apiURL, json={'chat_id': chat_id, 'text': message})
        print(response.text)
    except Exception as e:
        print(e)



sent_cnt = 0
def handle_socket_message(msg):
    global sent_cnt 
    if(sent_cnt > 3): 
        # sys.exit("done!")
        return
    try:
        data = msg['data']
        symbol = data['s']
        price = data['p']
        for condition in conditions:
            if condition['pair'] ==  symbol:
                if (condition['direction'] == '>' and float(price) > float(condition['price'])):
                    send_tg(price)
                    sent_cnt = sent_cnt+1
                    print(price)
                if (condition['direction'] == '<' and float(price) < float(condition['price'])):
                    sent_cnt = sent_cnt+1
                    send_tg(price)
                    print(price)
    except KeyError:
        # Key is not present
        pass

def main():
    twm = ThreadedWebsocketManager()
    twm.start()
    twm.start_multiplex_socket(callback=handle_socket_message, streams=streams)
    twm.join()


if __name__ == "__main__":
   main()
