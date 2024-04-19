#!/home/alex85/data/scripts/python/binance/binance_venv/bin/python

import csv
import pandas as pd
import matplotlib.pyplot as plt
from termcolor import colored

def csv_file_to_list():
    results = []
    with open("eth.csv") as csvfile:
        reader = csv.reader(csvfile) 
        columns_names = next(reader)
        columns_names = ['Index'] + columns_names[1:]
        for row in reader: 
            results.append(row)
    return [columns_names, results]

def formate_df(df):
    df['Open'] = df['Open'].astype(float).fillna(0.0)
    df['High'] = df['High'].astype(float).fillna(0.0)
    df['Low'] = df['Low'].astype(float).fillna(0.0)
    df['Close'] = df['Close'].astype(float).fillna(0.0)
    return df




def main():
    columns_names, kandles =  csv_file_to_list()
    df = pd.DataFrame(kandles)
    df.columns = columns_names
    df = formate_df(df)

    id_min = list(df[['Low']].idxmin())[0]

    df = df.iloc[id_min:, ]
    df = df.reset_index(drop=True)


    low_col = df['Low']

    min_price = low_col.min().tolist()
    max_price = low_col.max().tolist()
    last_price = low_col.iloc[-1];
    print(last_price,min_price,max_price) 

    min_pers = last_price / min_price * 100
    max_pers = -(100 - (last_price / max_price * 100))

    max_pers = '{}%'.format( round(max_pers, 2) )
    min_pers = '{}%'.format( round(min_pers, 2) )
    # print(min_pers, max_pers)
    print( colored(min_pers, 'green'),colored(max_pers, 'red'))
    # print(df)

    # df = df.iloc[-1000:, ]
    # print(list(df['Index']))
    # print(id_min)
    # plt.plot(list(df['Index']), list(df['Low']))
    # plt.show()
    # print(df)
    # df = df.drop([0,2])


if __name__ == "__main__":
    main()
