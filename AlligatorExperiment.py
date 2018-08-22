from TechnicalAnalysis import *
import time
#import datetime


class AlligatorExperiment(WilliamsIndicators):

    def __init__(self, currency_dict, time_interval):
        BinanceConnect.__init__(self, currency_dict, time_interval)
        #WilliamsIndicators.__init__(self)
        self.trading_decisions = pd.DataFrame(columns=['buy/sell', 'time', 'price', 'stop loss', \
        self.currency1 + '_balance', self.currency2 + '_balance'])
        self.stop_loss = False
        self.filename = self.currency_pair+'_'+self.time_interval+'_'+'trading_decisions.csv'
        self.climbing_price = 0
        self.candles_all_time = self.get_candles_list_all_time(self.currency_pair, self.time_interval)




    def theoretical_buy_historical(self, two_candles_list):
        '''
        always buy self.currency1, sell self.currency2
        candles indicies: 0 - Open time, 1 - Open, 2 - High, 3 - Low, 4 - Close, 5 - Volume, 6 - Close time
        '''

        #check available balance
        if self.currency_pair_dict[self.currency2] == 0:
            return

        # get buy data
        buy_price = float(two_candles_list[1][4])
        buy_time = datetime.fromtimestamp(two_candles_list[1][6] / 1000)
        buy_sell = 'buy'

        #update balances. buy for all available budget
        currency1_balance = self.currency_pair_dict[self.currency1]
        currency1_balance += self.currency_pair_dict[self.currency2] / buy_price
        self.currency_pair_dict[self.currency1] = currency1_balance
        self.currency_pair_dict[self.currency2] = 0

        #save trade data to list
        # save it to list
        trading_decisions_list = []

        trading_decisions_list.append(buy_sell)
        trading_decisions_list.append(buy_time)
        trading_decisions_list.append(buy_price)
        trading_decisions_list.append(self.stop_loss)
        trading_decisions_list.append(self.currency_pair_dict[self.currency1])
        trading_decisions_list.append(self.currency_pair_dict[self.currency2])

        # append decision to dataframe
        self.trading_decisions.loc[len(self.trading_decisions)] = trading_decisions_list



        self.stop_loss = False


    def theoretical_sell_historical(self, two_candles_list):
        '''
        always sell self.currency2, buy self.currency1
        candles indicies: 0 - Open time, 1 - Open, 2 - High, 3 - Low, 4 - Close, 5 - Volume, 6 - Close time
        '''

        # check available balance
        if self.currency_pair_dict[self.currency1] == 0:
            return

        # get buy data
        sell_price = float(two_candles_list[1][4])
        sell_time = datetime.fromtimestamp(two_candles_list[1][6] / 1000)
        buy_sell = 'sell'

        # update balances. buy for all available budget
        currency2_balance = self.currency_pair_dict[self.currency2]
        currency2_balance += self.currency_pair_dict[self.currency1] * sell_price
        self.currency_pair_dict[self.currency2] = currency2_balance
        self.currency_pair_dict[self.currency1] = 0

        # save trade data to list
        # save it to list
        trading_decisions_list = []

        trading_decisions_list.append(buy_sell)
        trading_decisions_list.append(sell_time)
        trading_decisions_list.append(sell_price)
        trading_decisions_list.append(self.stop_loss)
        trading_decisions_list.append(self.currency_pair_dict[self.currency1])
        trading_decisions_list.append(self.currency_pair_dict[self.currency2])

        # append decision to dataframe
        self.trading_decisions.loc[len(self.trading_decisions)] = trading_decisions_list

        # # save to file
        # path = '/Volumes/Data/Dropbox/Dropbox/Coding/BinanceTrade/current_experiment/'
        # self.trading_decisions.to_csv(path + self.filename)


    def theoretical_stop_loss_historical(self, two_candles_list):
        '''
        stop_loss is bitcoin optimized
        :param two_candles_dataframe:  last 2 candles in chronological order, earlier one first
        :return: None. Runs theoretical_sell to prevent losses
        candles indicies: 0 - Open time, 1 - Open, 2 - High, 3 - Low, 4 - Close, 5 - Volume, 6 - Close time
        '''
        if len(self.trading_decisions) < 1:
            return

        # if self.currency_pair_dict[self.currency1] != 0:
        #     return

        if self.currency_pair_dict[self.currency1] > 0:
            if float(two_candles_list[1][4]) < float(self.trading_decisions['price'][len(self.trading_decisions) - 1]) * 0.99:
                self.stop_loss = True
                self.theoretical_sell_historical(two_candles_list)


    def theoretical_buy_instant(self, two_candles_list):
        '''
        always buy self.currency1, sell self.currency2
        candles indicies: 0 - Open time, 1 - Open, 2 - High, 3 - Low, 4 - Close, 5 - Volume, 6 - Close time
        '''

        #check available balance
        if self.currency_pair_dict[self.currency2] == 0:
            return

        # get buy data
        buy_time = datetime.datetime.now()
        buy_price = self.get_current_buy_price()
        buy_sell = 'buy'

        #update balances. buy for all available budget
        currency1_balance = self.currency_pair_dict[self.currency1]
        currency1_balance += self.currency_pair_dict[self.currency2] / buy_price
        self.currency_pair_dict[self.currency1] = currency1_balance
        self.currency_pair_dict[self.currency2] = 0

        #save trade data to list
        # save it to list
        trading_decisions_list = []

        trading_decisions_list.append(buy_sell)
        trading_decisions_list.append(buy_time)
        trading_decisions_list.append(buy_price)
        trading_decisions_list.append(self.stop_loss)
        trading_decisions_list.append(self.currency_pair_dict[self.currency1])
        trading_decisions_list.append(self.currency_pair_dict[self.currency2])

        # append decision to dataframe
        self.trading_decisions.loc[len(self.trading_decisions)] = trading_decisions_list

        # save to file
        path = '/Users/Lao/Dropbox/Coding/BinanceTrade/current_experiment/'
        self.trading_decisions.to_csv(path + self.filename)

        self.stop_loss = False

    def theoretical_sell_instant(self, two_candles_list):
        '''
        always sell self.currency2, buy self.currency1
        candles indicies: 0 - Open time, 1 - Open, 2 - High, 3 - Low, 4 - Close, 5 - Volume, 6 - Close time
        '''

        # check available balance
        if self.currency_pair_dict[self.currency1] == 0:
            return

        # get buy data
        sell_price = self.get_current_sell_price()
        sell_time = datetime.datetime.now()
        buy_sell = 'sell'

        # update balances. buy for all available budget
        currency2_balance = self.currency_pair_dict[self.currency2]
        currency2_balance += self.currency_pair_dict[self.currency1] * sell_price
        self.currency_pair_dict[self.currency2] = currency2_balance
        self.currency_pair_dict[self.currency1] = 0

        # save trade data to list
        # save it to list
        trading_decisions_list = []

        trading_decisions_list.append(buy_sell)
        trading_decisions_list.append(sell_time)
        trading_decisions_list.append(sell_price)
        trading_decisions_list.append(self.stop_loss)
        trading_decisions_list.append(self.currency_pair_dict[self.currency1])
        trading_decisions_list.append(self.currency_pair_dict[self.currency2])

        # append decision to dataframe
        self.trading_decisions.loc[len(self.trading_decisions)] = trading_decisions_list

        # save to file
        path = '/Users/Lao/Dropbox/Coding/BinanceTrade/current_experiment/'
        self.trading_decisions.to_csv(path + self.filename)


    def climbing_stop_loss(self, two_candles_list):
        '''
        if price goes up - stop_loss barrier moves up
        :return: None. Runs theoretical_sell to prevent losses
        candles indicies: 0 - Open time, 1 - Open, 2 - High, 3 - Low, 4 - Close, 5 - Volume, 6 - Close time
        '''

        if self.currency_pair_dict[self.currency2] != 0:
            return

        #try if there are any deals yet
        if self.climbing_price == 0:
            try:
                buy_price = self.trading_decisions['price'][len(self.trading_decisions) - 1]
            except:
                return

        #if close price is higher than climbing - increase climbing price
        if  self.climbing_price < float(two_candles_list[1][4]):
            self.climbing_price = float(two_candles_list[1][4])

        #actual stop loss
        if self.climbing_price > float(two_candles_list[1][4]) * 0.98:
            self.stop_loss = True
            self.theoretical_sell_historical(two_candles_list)


    def stoploss_last5low(self, two_candles_list, two_candles_index):
        #stoploss is always equal to minimum of last 5 candles low

        if self.currency_pair_dict[self.currency1] == 0:
            return

        try:
            candles5_list = self.candles_all_time[(two_candles_index - 3):(two_candles_index + 2)]
        except:
            return

        low_list = []

        for el in candles5_list:
            low_list.append(float(el[3]))

        try:
            stop_price = min(low_list)
        except:
            return

        if float(two_candles_list[1][4]) < stop_price:
            self.stop_loss = True
            self.theoretical_sell_historical(two_candles_list)




    def div_bar_alligator_distance(self):

        # measure script run time
        start_time = time.time()

        for i in range(len(self.candles_all_time) - 1):

            two_candles_list = self.candles_all_time[i:i + 2]
            two_candles_index = i

            # checks
            #self.theoretical_stop_loss_historical(two_candles_list)
            #self.climbing_stop_loss(two_candles_list)
            self.stoploss_last5low(two_candles_list, two_candles_index)

            #buy
            if self.check_bull_bar(two_candles_list) and \
            self.distance_between_alligator_and_candles(two_candles_list, two_candles_index):
                self.theoretical_buy_historical(two_candles_list)

            #sell
            try:
                if self.check_bear_bar(two_candles_list) and (float(two_candles_list[1][4]) > \
                    float(self.trading_decisions['price'][len(self.trading_decisions) - 1])) \
                    and self.distance_between_alligator_and_candles(two_candles_list, two_candles_index):
                    self.theoretical_sell_historical(two_candles_list)
            except:
                self.theoretical_sell_historical(two_candles_list)

        # measure script run time
        print('running time', time.time() - start_time, 'sec.')

        # save to file
        path = '/Users/Lao/Dropbox/Coding/BinanceTrade/current_experiment/'
        self.trading_decisions.to_csv(path + self.filename)


    def create_metrics_dataframe(self):
        '''
        :return: dataframe with open time, trend_direction, bar_type, profitunity_windows
        candles indicies: 0 - Open time, 1 - Open, 2 - High, 3 - Low, 4 - Close, 5 - Volume, 6 - Close time
        '''

        metrics_dataframe = pd.DataFrame(columns=['Open time','trend_direction', 'bar_type', 'profitunity_window'])


        for i in range(len(self.candles_all_time) - 1):
            metrics_list = []
            two_candles_list = self.candles_all_time[i:i+2]


            open_time = datetime.fromtimestamp(self.candles_all_time[i][0] / 1000)
            trend_direction = self.trend_direction(two_candles_list)
            bar_type = self.check_bar_type(two_candles_list)
            profitunity_window = self.profitunity_windows(two_candles_list)

            metrics_list.append(open_time)
            metrics_list.append(trend_direction)
            metrics_list.append(bar_type)
            metrics_list.append(profitunity_window)

            metrics_dataframe.loc[len(metrics_dataframe)] = metrics_list

        candles_dataframe = self.get_n_candles_as_dataframe(len(self.candles_all_time))

        all_dataframe = candles_dataframe.merge(metrics_dataframe, on='Open time', how = 'inner')

        all_dataframe.to_csv('all_dataframe.csv')


    def score_trend_bar_window(self, two_candles_list):
        '''
        :param two_candles_list:
        :return: score: +10 if trend + or -, +2 for strong bar type signals(31, 13), +1 for medium (23, 21)
        '''
        pass

    def div_bar_alligator_angularation(self):


        for i in range(len(self.candles_all_time) - 1):
            two_candles_list = self.candles_all_time[i:i + 2]
            two_candles_index = i
            trend_direction = self.trend_direction(two_candles_list)
            #bar_type = self.check_bar_type(two_candles_list)
            profitunity_window = self.profitunity_windows(two_candles_list)

            self.stoploss_last5low(two_candles_list, two_candles_index)
            #self.climbing_stop_loss(two_candles_list)

            if trend_direction == '+' and profitunity_window == 'green':
                self.theoretical_buy_historical(two_candles_list)
            elif trend_direction == '-' and profitunity_window == 'green':
                self.theoretical_sell_historical(two_candles_list)

        # save to file
        path = '/Users/Lao/Dropbox/Coding/BinanceTrade/current_experiment/'
        self.trading_decisions.to_csv(path + self.filename)


    def div_bar_alligator_angularation(self):
        '''
        Runs experiment.
        Stop loss 1%
        divergent bar, alligator distance, angularation
        :return: None
        '''

        # measure script run time
        start_time = time.time()

        for i in range(len(self.candles_all_time) - 1):

            two_candles_list = self.candles_all_time[i:i + 2]
            two_candles_index = i

            # checks
            #self.theoretical_stop_loss_historical(two_candles_list)
            self.climbing_stop_loss(two_candles_list)
            #self.stoploss_last5low(two_candles_list, two_candles_index)

            #buy
            if self.check_bull_bar(two_candles_list) and \
            self.distance_between_alligator_and_candles(two_candles_list, two_candles_index) and self.angularation(two_candles_index):
                self.theoretical_buy_historical(two_candles_list)

            #sell
            try:
                if self.check_bear_bar(two_candles_list) and (float(two_candles_list[1][4]) > \
                    float(self.trading_decisions['price'][len(self.trading_decisions) - 1])) \
                    and self.distance_between_alligator_and_candles(two_candles_list, two_candles_index):
                    self.theoretical_sell_historical(two_candles_list) and self.angularation(two_candles_index)
            except:
                self.theoretical_sell_historical(two_candles_list)

        # measure script run time
        print('running time', time.time() - start_time, 'sec.')

        # save to file
        path = '/Users/Lao/Dropbox/Coding/BinanceTrade/current_experiment/'
        self.trading_decisions.to_csv(path + self.filename)




# measure script run time
start_time = time.time()


currency_dict = {'LTC': 0, 'USDT': 100}
time_interval = Client.KLINE_INTERVAL_2HOUR
AE = AlligatorExperiment(currency_dict, time_interval)
AE.div_bar_alligator_angularation()
#AE.div_bar_alligator_experiment()
#AE.trend_bar_window_experiment()


# measure script run time
print('Total time', time.time() - start_time, 'sec.')


