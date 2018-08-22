from BinanceConnect import *



class BinanceConnectTest(BinanceConnect):
    def __init__(self):


        self.currency_pair_dict = {'BTC': 1, 'USDT': 0}
        self.time_interval= Client.KLINE_INTERVAL_1MINUTE

        self.BC_test_class = BinanceConnect(self.currency_pair_dict, self.time_interval)
        BinanceConnect.__init__(self)

        #self.time_interval = client


    def test_init(self):
        print(self.BC_test_class.currency_pair_dict)
        print(self.BC_test_class.time_interval)
        print(self.BC_test_class.currency_pair)
        print(self.BC_test_class.client)


    def test_connect(self):
        print(self.BC_test_class.get_candles_list(self.BC_test_class.currency_pair, self.BC_test_class.time_interval))
        print(len(self.BC_test_class.get_candles_list(self.BC_test_class.currency_pair, self.BC_test_class.time_interval)))


    def test_get_n_candles(self):
        print(self.BC_test_class.get_n_candles_as_dataframe(2))
        print(self.BC_test_class.get_n_candles_as_dataframe(13))


    def test_get_available_currency_pairs_list(self):
        print(self.BC_test_class.get_available_currency_pairs_list())




        
        
x = BinanceConnectTest()
#x.test_init()
#x.test_connect()
#x.test_get_n_candles()
#x.test_get_available_currency_pairs_list()
print(x.get_n_candles_as_dataframe(20))

# depthb = x.get_current_buy_price()
# depths = x.get_current_sell_price()

# print(depthb)
# print(depths)