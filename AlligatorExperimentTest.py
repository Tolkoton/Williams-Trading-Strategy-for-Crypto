from AlligatorExperiment import *

class AlligatorExperimentTest(AlligatorExperiment):

    def __init__(self, currency_dict, time_interval):
        BinanceConnect.__init__(self, currency_dict, time_interval)
        self.candles_all_time = self.get_candles_list_all_time(self.currency_pair, self.time_interval)

    def test_init(self):
        test_class = AlligatorExperiment()
        print(test_class)
        print(type(self.currency_pair_dict.keys()))
        print(self.currency1)
        print(self.currency2)
        print(self.currency1_balance)
        print(self.currency2_balance)
        print(self.filename)
        print(self.trading_decisions)
        self.all_candles = self.get_candles_list(self.currency_pair, self.time_interval)


    def test_theoretical_buy_historical(self):
        two_candles_list = self.all_candles[-2:]
        self.theoretical_buy_historical(two_candles_list)
        print(self.trading_decisions)


    def test_theoretical_sell_historical(self):
        two_candles_list = self.all_candles[-2:]
        self.theoretical_sell_historical(two_candles_list)
        print(self.trading_decisions)


    def test_climbing_stop_loss(self):
        two_candles_list = self.all_candles[-2:]
        print(self.climbing_stop_loss(two_candles_list))


    def test_div_bar_alligator_experiment(self):
        print(self.div_bar_alligator_angularation())


    def test_create_metrics_dataframe(self):
        self.create_metrics_dataframe()


    def test_trend_bar_window_experiment(self):
        for i in range(len(self.candles_all_time) - 1):
            two_candles_list = self.candles_all_time[i:i+2]
            print(self.trend_bar_window_experiment(two_candles_list))







currency_dict = {'BTC': 1, 'USDT': 0}
time_interval = Client.KLINE_INTERVAL_2HOUR
x = AlligatorExperimentTest(currency_dict, time_interval)

# #x.test_init()
# # x.test_theoretical_buy_historical()
# # x.test_theoretical_sell_historical()
# #x.test_climbing_stop_loss()
# #x.test_div_bar_alligator_experiment()
#
# print(x.currency_pair, x.time_interval)
#x.test_create_metrics_dataframe()

x.test_trend_bar_window_experiment()
