from ExperimentDivergentBarAlligator import *


start_time = time.time()

class TestExperimentDivergentBarAlligator(ExperimentDivergentBarAlligator):

    def __init__(self):
        ExperimentDivergentBarAlligator.__init__(self)
        self.EXBA_test = ExperimentDivergentBarAlligator()

    def test_init(self):
        print(self.EXBA_test)
        print(self.EXBA_test.deal)
        print(self.EXBA_test.total_profit)
        print(self.EXBA_test.trading_decisions)


    def test_theoretical_buy(self):

        print('Test theoretical_buy')

        two_candles_dataframe = self.EXBA_test.get_n_candles_as_dataframe(2)
        print(two_candles_dataframe)

        self.EXBA_test.theoretical_buy_instant(two_candles_dataframe)
        print(self.EXBA_test.trading_decisions)
        print(self.EXBA_test.deal, '\n')

    def test_theoretical_sell(self):

        print('Test theoretical_sell')
        two_candles_dataframe = self.EXBA_test.get_n_candles_as_dataframe(2)
        #self.EXBA_test.deal = False
        self.EXBA_test.theoretical_sell_instant(two_candles_dataframe)
        print(self.EXBA_test.trading_decisions)
        print(self.EXBA_test.deal, '\n')


    def test_buy_sell_stop_loss(self):

        all_candles = self.EXBA_test.get_n_candles_as_dataframe(1000)
        two_candles_dataframe = pd.DataFrame(columns=all_candles.columns)

        #run all test cases for last 1000 candles
        for i in range(len(all_candles ) - 1):
            # create two_candles_dataframe
            candle0 = all_candles.loc[i]
            candle1 = all_candles.loc[i + 1]
            two_candles_dataframe.loc[0] = candle0
            two_candles_dataframe.loc[1] = candle1

            #checks
            self.EXBA_test.theoretical_stop_loss_historical(two_candles_dataframe)

            if self.EXBA_test.check_bull_bar_dataframe(two_candles_dataframe):
                self.EXBA_test.theoretical_buy_historical(two_candles_dataframe)

            try:
                if self.EXBA_test.check_bear_bar_dataframe(two_candles_dataframe) and (float(candle1['Close'])) > \
                        1.001*float(self.EXBA_test.trading_decisions['price'][len(self.EXBA_test.trading_decisions) - 1]):
                         self.EXBA_test.theoretical_sell_historical(two_candles_dataframe)
            except:
                pass


    def test_buy_sell_stop_loss_alligator(self):

        WI_class = WilliamsIndicators()

        all_candles = self.EXBA_test.get_n_candles_as_dataframe(1000)
        two_candles_dataframe = pd.DataFrame(columns=all_candles.columns)

        # run all test cases for last 1000 candles
        for i in range(len(all_candles) - 1):
            # create two_candles_dataframe
            candle0 = all_candles.loc[i]
            candle1 = all_candles.loc[i + 1]
            two_candles_dataframe.loc[0] = candle0
            two_candles_dataframe.loc[1] = candle1

            all_candles_list = self.get_candles_list(self.currency_pair, self.time_interval)
            two_candles_list = all_candles_list[i:i+2]
            two_candles_index = i

            # checks
            self.EXBA_test.theoretical_stop_loss_historical(two_candles_dataframe)


            if self.EXBA_test.check_bull_bar_dataframe(two_candles_dataframe) and \
            WI_class.distance_between_alligator_and_candles(two_candles_list, two_candles_index):
                self.EXBA_test.theoretical_buy_historical(two_candles_dataframe)

            try:
                if self.EXBA_test.check_bear_bar_dataframe(two_candles_dataframe) and (float(candle1['Close'])) > \
                1.001 * float(self.EXBA_test.trading_decisions['price'][len(self.EXBA_test.trading_decisions) - 1]) \
                and WI_class.distance_between_alligator_and_candles(two_candles_list, two_candles_index):
                    self.EXBA_test.theoretical_sell_historical(two_candles_dataframe)
            except:
                pass


x = TestExperimentDivergentBarAlligator()
#x.test_buy_sell_stop_loss()
x.test_buy_sell_stop_loss_alligator()
print("time elapsed: {:.2f}s".format(time.time() - start_time))



