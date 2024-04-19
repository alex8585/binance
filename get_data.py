#!/home/alex85/data/scripts/python/binance/binance_venv/bin/python

import csv
import pandas as pd
import sys
from binance.client import Client
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('API_KEY')
api_secret = os.getenv('API_SECRET')

client = Client(api_key, api_secret)


def main():
    client = Client(api_key, api_secret)
    # candles = client.get_klines(symbol='ETHUSDT', interval=Client.KLINE_INTERVAL_30MINUTE)
    klines = client.get_historical_klines("ETHUSDT", Client.KLINE_INTERVAL_1HOUR, "1 Jan, 2022")
    df = pd.DataFrame(klines)

    df.columns = ['a1', 'Open', 'High', 'Low','Close','a2','a3','a4','a5','a6','a7','a8']

    df = df.drop( ['a1','a2','a3','a4','a5','a6','a7','a8'], axis = 1 )

    df['Open'] = df['Open'].astype(float).fillna(0.0)
    df['High'] = df['High'].astype(float).fillna(0.0)
    df['Low'] = df['Low'].astype(float).fillna(0.0)
    df['Close'] = df['Close'].astype(float).fillna(0.0)
    # df['Open'] = df['Open'].apply(lambda x: '{:,.2f}'.format(x))

    df.to_csv("eth.csv")
    print(df)



if __name__ == "__main__":
    main()













