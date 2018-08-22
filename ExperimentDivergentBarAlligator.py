#TODO деякі функції працюють з датафрейм, деякі вже зі списком. Треба буде перевести все на список. Так набагато швидше
#TODO
from TechnicalAnalysis import *
import time
import datetime
import pandas as pd



class ExperimentDivergentBarAlligator(WilliamsIndicators):
    '''
        runs experiment making trading decisions using divergent bars and alligator
    '''

    def __init__(self):
        WilliamsIndicators.__init__(self)
        self.stop_loss = False
        self.deal = False
        self.total_profit = 0
        self.trading_decisions = pd.DataFrame(columns=['buy/sell', 'time', 'price', 'stop loss', 'profit', 'total profit'])


    def theoretical_buy_instant(self, two_candles_dataframe):
        '''
            doesnt make any decision, just buy
            :param two_candles_dataframe: last 2 candles in chronological order, earlier one first
            :return: None, saves decision to file
         '''

        if not self.deal:
            # get buy data
            buy_time = datetime.datetime.now()
            buy_price = self.get_current_buy_price()
            buy_sell = 'buy'
            profit = 0

            # save it to list
            trading_decisions_list = []

            trading_decisions_list.append(buy_sell)
            trading_decisions_list.append(buy_time)
            trading_decisions_list.append(buy_price)
            trading_decisions_list.append(self.stop_loss)
            trading_decisions_list.append(profit)
            trading_decisions_list.append(self.total_profit)

            # append decision to dataframe
            self.trading_decisions.loc[len(self.trading_decisions)] = trading_decisions_list

            # save to file
            self.trading_decisions.to_csv('trading_decisions.csv')

            # change deal flag to prevent buy before selling. Emulating no balance
            self.deal = True


    def theoretical_sell_instant(self, two_candles_dataframe):
        '''
        doesnt make any decision, just sell
        :param two_candles_dataframe: last 2 candles in chronological order, earlier one first
        :return: None, saves decision to file
        '''

        if self.deal:
            # get sell data
            sell_price = self.get_current_sell_price()
            sell_time = datetime.datetime.now()
            buy_sell = 'sell'
            profit = sell_price - float(self.trading_decisions['price'][len(self.trading_decisions) - 1])
            self.total_profit += profit

            # save it to list
            trading_decisions_list = []
            trading_decisions_list.append(buy_sell)
            trading_decisions_list.append(sell_time)
            trading_decisions_list.append(sell_price)
            trading_decisions_list.append(self.stop_loss)
            trading_decisions_list.append(profit)
            trading_decisions_list.append(self.total_profit)

            # append decision to dataframe
            self.trading_decisions.loc[len(self.trading_decisions)] = trading_decisions_list

            # save to file
            self.trading_decisions.to_csv('trading_decisions.csv')

            # change deal flag to prevent buy before selling. Emulating no balance
            self.deal = False
            self.stop_loss = False

    def theoretical_stop_loss_instant(self, two_candles_dataframe):
        '''
                :param two_candles_dataframe:  last 2 candles in chronological order, earlier one first
                :return: None. Runs theoretical_sell to prevent losses
                '''
        if self.deal and float(two_candles_dataframe['Close'][1]) < float(
                self.trading_decisions['price'][len(self.trading_decisions) - 1]) * 0.99:
            self.stop_loss = True
            self.theoretical_sell_instant(two_candles_dataframe)


    def theoretical_buy_historical(self, two_candles_dataframe):
        '''
            doesnt make any decision, just buy
            :param two_candles_dataframe: last 2 candles in chronological order, earlier one first
            :return: None, saves decision to file
         '''

        if not self.deal:
            # get buy data

            buy_price = float(two_candles_dataframe['Close'][1])
            buy_time = two_candles_dataframe['Close time'][1]
            buy_sell = 'buy'
            profit = 0

            # save it to list
            trading_decisions_list = []

            trading_decisions_list.append(buy_sell)
            trading_decisions_list.append(buy_time)
            trading_decisions_list.append(buy_price)
            trading_decisions_list.append(self.stop_loss)
            trading_decisions_list.append(profit)
            trading_decisions_list.append(self.total_profit)

            # append decision to dataframe
            self.trading_decisions.loc[len(self.trading_decisions)] = trading_decisions_list

            # save to file
            self.trading_decisions.to_csv('trading_decisions.csv')

            # change deal flag to prevent buy before selling. Emulating no balance
            self.deal = True


    def theoretical_sell_historical(self, two_candles_dataframe):
        '''
        doesnt make any decision, just sell
        :param two_candles_dataframe: last 2 candles in chronological order, earlier one first
        :return: None, saves decision to file
        '''

        if self.deal:
            # get sell data
            sell_time = two_candles_dataframe['Close time'][1]
            sell_price = float(two_candles_dataframe['Close'][1])
            buy_sell = 'sell'
            profit = sell_price - float(self.trading_decisions['price'][len(self.trading_decisions) - 1])
            self.total_profit += profit

            # save it to list
            trading_decisions_list = []
            trading_decisions_list.append(buy_sell)
            trading_decisions_list.append(sell_time)
            trading_decisions_list.append(sell_price)
            trading_decisions_list.append(self.stop_loss)
            trading_decisions_list.append(profit)
            trading_decisions_list.append(self.total_profit)

            # append decision to dataframe
            self.trading_decisions.loc[len(self.trading_decisions)] = trading_decisions_list

            # save to file
            print(self.trading_decisions)
            self.trading_decisions.to_csv('trading_decisions.csv')

            # change deal flag to prevent buy before selling. Emulating no balance
            self.deal = False
            self.stop_loss = False


    def theoretical_stop_loss_historical(self, two_candles_dataframe):
        '''
                :param two_candles_dataframe:  last 2 candles in chronological order, earlier one first
                :return: None. Runs theoretical_sell to prevent losses
        '''
        if self.deal and float(two_candles_dataframe['Close'][1]) < float(
                self.trading_decisions['price'][len(self.trading_decisions) - 1]) * 0.9:
            self.stop_loss = True
            self.theoretical_sell_historical(two_candles_dataframe)


    def experiment_div_bar(self):

        two_candles_dataframe = self.get_n_candles_as_dataframe(2)
        # checks
        self.theoretical_stop_loss_instant(two_candles_dataframe)

        if self.check_bull_bar_dataframe(two_candles_dataframe):
            self.theoretical_buy_instant(two_candles_dataframe)

        try:
            if self.check_bear_bar_dataframe(two_candles_dataframe) and (float(two_candles_dataframe['Close'][1])) > \
                    1.001 * float(self.trading_decisions['price'][len(self.trading_decisions) - 1]):
                self.theoretical_sell_instant(two_candles_dataframe)
        except:
            pass


    def run_experiment_div_bar(self):
        while True:
            start_time = time.time()
            self.experiment_div_bar()
            time.sleep(60 - (time.time() - start_time))


# x = ExperimentDivergentBarAlligator()
# x.run_experiment_div_bar()

