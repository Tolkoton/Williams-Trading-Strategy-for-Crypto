import pandas as pd
from binance.client import Client
from datetime import datetime


class BinanceConnect(object):
    '''
    Class BinanceConnect connects to Binance and gets all the data from API
    Takes in a currency_pair_dict with currency names and balance for each currency and time interval for candles
    functions: connect(to Binance), get all candles, get a dataframe from given amount of candles
    '''
    def __init__(self, currency_pair_dict = {'LTC': 1, 'USDT': 0}, time_interval = Client.KLINE_INTERVAL_2HOUR):

        self.currency_pair_dict = currency_pair_dict
        self.time_interval = time_interval
        self.currency1 = str(list(self.currency_pair_dict.keys())[0])
        self.currency2 = str(list(self.currency_pair_dict.keys())[1])
        self.currency_pair = self.currency1 + self.currency2

        #connect to Binance
        self.client = self.connect()

        #get candles
        self.candles_all_time = self.get_candles_list_all_time(self.currency_pair, self.time_interval)


    def connect(self):
        # conects to Binance and returns Binance client

        # Binance Api data
        api_key = 'ENTER YOUR API'
        api_secret = 'ENTER YOUR SECRET CODE'

        # connect Binance
        return Client(api_key, api_secret)


    def get_candles_list(self, currency_pair, time_interval, limit = 1000):
        #returns last 1000 candles as list

        # klines/candlesticks
        candles = self.client.get_klines(symbol=currency_pair, interval=time_interval, limit=limit)

        return candles


    def get_candles_list_all_time(self, currency_pair, time_interval):
        # returns candles as list from given date till now

        # klines/candlesticks
        candles = self.client.get_historical_klines(currency_pair, time_interval, "1 Feb, 2018")

        return candles


    def get_n_candles_as_dataframe(self, n):
        # returns a dataframe with given amount of candles, n

        # create empty dataframe for candles
        candles_dataframe = pd.DataFrame(columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', \
                     'Quote asset volume', 'Number of trades', 'Taker buy base asset volume','Taker buy quote asset volume', \
                     'Can be ignored'])

        last_n_rows = self.get_candles_list(self.currency_pair, self.time_interval)[-n:]

        for i in range(len(last_n_rows)):
            last_n_rows[i][0] = datetime.fromtimestamp(last_n_rows[i][0] / 1000)
            last_n_rows[i][6] = datetime.fromtimestamp(last_n_rows[i][6] / 1000)
            candles_dataframe.loc[i] = last_n_rows[i]

        candles_dataframe = candles_dataframe.drop(columns='Can be ignored')

        return candles_dataframe


    def get_available_currency_pairs_list(self):
        #returns a list of currency pairs available on Binance so they can be used in client.get_klines
        data = self.client.get_exchange_info()
        symbol_list = []

        for i in range(len((data['symbols']))):
            symbol_list.append(data['symbols'][i]['symbol'])

        return symbol_list


    def get_current_buy_price(self, amount = 1):
        '''
        gets current buy price from order book. If best ask offers lower amount of currency than we need to buy -
        get the rest from lower ones
        '''
        buy_price = 0
        i = 0
        depth = self.client.get_order_book(symbol=self.currency_pair)

        while amount > 0:
            # if best offer has enough currency - return its price
            if amount <= float(depth['asks'][i][1]):
                buy_price += amount * float(depth['asks'][i][0])
                amount = 0
                return buy_price

            #else compute average price from different sources
            else:
                amount -= float(depth['asks'][i][1])
                buy_price += float(depth['asks'][i][1]) * float(depth['asks'][i][0])

            i += 1



    def get_current_sell_price(self, amount = 1):
        '''
        gets current sell price from order book
        If best bid offers lower amount of currency than we need to sell -
        get the rest from lower ones
        :return:
        '''
        sell_price = 0
        i = 0
        depth = self.client.get_order_book(symbol=self.currency_pair)

        while amount > 0:
            # if best offer has enough currency - return its price
            if amount <= float(depth['bids'][i][1]):
                sell_price += amount * float(depth['bids'][i][0])
                amount = 0
                return sell_price

            # else compute average price from different sources
            else:
                amount -= float(depth['bids'][i][1])
                sell_price += float(depth['bids'][i][1]) * float(depth['bids'][i][0])

            i += 1




