import glob
#import pandas as pd
from AlligatorExperiment import *


class TableAnalyzer(AlligatorExperiment):
#allows to runs different experiments at once.


    def __init__(self):
        pass


    def instance_generator(self):
        #creates separate instances for running experiments from currencies_list and time_intervals_list
        currencies_list =['BTC', 'ETH', 'LTC', 'ADA', 'XRP']
        time_intervals_list = [Client.KLINE_INTERVAL_1MINUTE, Client.KLINE_INTERVAL_5MINUTE, Client.KLINE_INTERVAL_15MINUTE, \
                               Client.KLINE_INTERVAL_30MINUTE, Client.KLINE_INTERVAL_1HOUR, Client.KLINE_INTERVAL_2HOUR]

        #time_intervals_list = [Client.KLINE_INTERVAL_1MINUTE]

        dict_list = []

        for cur in currencies_list:
            new_dic = {}
            new_dic[cur] = 0
            new_dic['USDT'] = 1000
            dict_list.append(new_dic)

        instances_list = [AlligatorExperiment(cur, time) for cur in dict_list for time in time_intervals_list]

        return instances_list


    def run_experiments_from_instance_list(self):
        #runs all experiments instance list

        instance_list = self.instance_generator()
        for instance in instance_list:
            instance.div_bar_alligator_angularation()



    def tables_summary(self):
        #summarizes results from all instance tests
        #TODO ? what if last balance in USDT? Do we need add this data to df? Currently adding last non USDT balance
        summary = pd.DataFrame(columns=['Currency Pair', 'Time Interval', 'Start Price', 'End Price', 'Start balance', 'End Balance'])
        path = '/Users/Lao/Dropbox/Coding/BinanceTrade/current_experiment/*.csv'
        savepath = '/Users/Lao/Dropbox/Coding/BinanceTrade/current_experiment/'
        files = glob.glob(path)

        for name in files:
            summary_list = []
            current_table = pd.read_csv(name)

            no_extension = name.split('/')[-1]

            try:
                currency_pair = no_extension.split('_')[0]
                time_interval = no_extension.split('_')[1]
            except:
                pass

            try:
                start_price = current_table['price'][0]
            except:
                pass

            start_balance = 100

            #end price, end balance. If last trade is buy USDT, ignore it, take previous trade data
            try:
                if current_table.iloc[-1][-1] == 0:
                    end_balance = current_table.iloc[-2][-1]
                    end_price = current_table.iloc[-2]['price']
                else:
                    end_balance = current_table.iloc[-1][-1]
                    end_price = current_table.iloc[-1]['price']
            except:
                pass

            summary_list.append(currency_pair)
            summary_list.append(time_interval)
            summary_list.append(start_price)
            summary_list.append(end_price)
            summary_list.append(start_balance)
            summary_list.append(end_balance)

            summary.loc[len(summary)] = summary_list

        summary.to_csv(savepath + 'summary.csv')


    def instance_runner_manual(self):
        currency1_balance = 0
        currency2_balance = 100

        # ada1 = AlligatorExperiment({'ADA': currency1_balance, 'USDT': currency2_balance}, time_interval = Client.KLINE_INTERVAL_1MINUTE)
        # ada1.div_bar_alligator_angularation()
        #
        # ada5 = AlligatorExperiment({'ADA': currency1_balance, 'USDT': currency2_balance}, time_interval=Client.KLINE_INTERVAL_5MINUTE)
        # ada5.div_bar_alligator_angularation()
        #
        # ada15 = AlligatorExperiment({'ADA': currency1_balance, 'USDT': currency2_balance}, time_interval=Client.KLINE_INTERVAL_15MINUTE)
        # ada15.div_bar_alligator_angularation()
        #
        # ada30 = AlligatorExperiment({'ADA': currency1_balance, 'USDT': currency2_balance}, time_interval=Client.KLINE_INTERVAL_30MINUTE)
        # ada30.div_bar_alligator_angularation()
        #
        # ada1h = AlligatorExperiment({'ADA': currency1_balance, 'USDT': currency2_balance}, time_interval=Client.KLINE_INTERVAL_1HOUR)
        # ada1h.div_bar_alligator_angularation()
        #
        # ada2h = AlligatorExperiment({'ADA': currency1_balance, 'USDT': currency2_balance}, time_interval=Client.KLINE_INTERVAL_2HOUR)
        # ada2h.div_bar_alligator_angularation()

        # btc1 = AlligatorExperiment({'BTC': currency1_balance, 'USDT': currency2_balance}, time_interval=Client.KLINE_INTERVAL_1MINUTE)
        # btc1.div_bar_alligator_angularation()

        # btc5 = AlligatorExperiment({'BTC': currency1_balance, 'USDT': currency2_balance}, time_interval=Client.KLINE_INTERVAL_5MINUTE)
        # btc5.div_bar_alligator_angularation()
        #
        # btc15 = AlligatorExperiment({'BTC': currency1_balance, 'USDT': currency2_balance}, time_interval=Client.KLINE_INTERVAL_15MINUTE)
        # btc15.div_bar_alligator_angularation()
        #
        # btc30 = AlligatorExperiment({'BTC': currency1_balance, 'USDT': currency2_balance}, time_interval=Client.KLINE_INTERVAL_30MINUTE)
        # btc30.div_bar_alligator_angularation()
        #
        # btc1h = AlligatorExperiment({'BTC': currency1_balance, 'USDT': currency2_balance}, time_interval=Client.KLINE_INTERVAL_1HOUR)
        # btc1h.div_bar_alligator_angularation()

        # btc2h = AlligatorExperiment({'BTC': currency1_balance, 'USDT': currency2_balance}, time_interval=Client.KLINE_INTERVAL_2HOUR)
        # btc2h.div_bar_alligator_angularation()

        # eth1 = AlligatorExperiment({'ETH': currency1_balance, 'USDT': currency2_balance}, time_interval=Client.KLINE_INTERVAL_1MINUTE)
        # eth1.div_bar_alligator_angularation()
        #
        # eth5 = AlligatorExperiment({'ETH': currency1_balance, 'USDT': currency2_balance}, time_interval=Client.KLINE_INTERVAL_5MINUTE)
        # eth5.div_bar_alligator_angularation()
        #
        # eth15 = AlligatorExperiment({'ETH': currency1_balance, 'USDT': currency2_balance}, time_interval=Client.KLINE_INTERVAL_15MINUTE)
        # eth15.div_bar_alligator_angularation()
        #
        # eth30 = AlligatorExperiment({'ETH': currency1_balance, 'USDT': currency2_balance}, time_interval=Client.KLINE_INTERVAL_30MINUTE)
        # eth30.div_bar_alligator_angularation()
        #
        # eth1h = AlligatorExperiment({'ETH': currency1_balance, 'USDT': currency2_balance}, time_interval=Client.KLINE_INTERVAL_1HOUR)
        # eth1h.div_bar_alligator_angularation()
        #
        # eth2h = AlligatorExperiment({'ETH': currency1_balance, 'USDT': currency2_balance}, time_interval=Client.KLINE_INTERVAL_2HOUR)
        # eth2h.div_bar_alligator_angularation()
        #
        # ltc1 = AlligatorExperiment({'LTC': currency1_balance, 'USDT': currency2_balance}, time_interval=Client.KLINE_INTERVAL_1MINUTE)
        # ltc1.div_bar_alligator_angularation()
        #
        # ltc5 = AlligatorExperiment({'LTC': currency1_balance, 'USDT': currency2_balance}, time_interval=Client.KLINE_INTERVAL_5MINUTE)
        # ltc5.div_bar_alligator_angularation()
        #
        # ltc15 = AlligatorExperiment({'LTC': currency1_balance, 'USDT': currency2_balance}, time_interval=Client.KLINE_INTERVAL_15MINUTE)
        # ltc15.div_bar_alligator_angularation()
        #
        # ltc30 = AlligatorExperiment({'LTC': currency1_balance, 'USDT': currency2_balance}, time_interval=Client.KLINE_INTERVAL_30MINUTE)
        # ltc30.div_bar_alligator_angularation()
        #
        # ltc1h = AlligatorExperiment({'LTC': currency1_balance, 'USDT': currency2_balance}, time_interval=Client.KLINE_INTERVAL_1HOUR)
        # ltc1h.div_bar_alligator_angularation()
        #
        # ltc2h = AlligatorExperiment({'LTC': currency1_balance, 'USDT': currency2_balance}, time_interval=Client.KLINE_INTERVAL_2HOUR)
        # ltc2h.div_bar_alligator_angularation()

        xrp1 = AlligatorExperiment({'XRP': currency1_balance, 'USDT': currency2_balance}, time_interval=Client.KLINE_INTERVAL_1MINUTE)
        xrp1.div_bar_alligator_angularation()

        xrp5 = AlligatorExperiment({'XRP': currency1_balance, 'USDT': currency2_balance}, time_interval=Client.KLINE_INTERVAL_5MINUTE)
        xrp5.div_bar_alligator_angularation()

        xrp15 = AlligatorExperiment({'XRP': currency1_balance, 'USDT': currency2_balance}, time_interval=Client.KLINE_INTERVAL_15MINUTE)
        xrp15.div_bar_alligator_angularation()

        xrp30 = AlligatorExperiment({'XRP': currency1_balance, 'USDT': currency2_balance}, time_interval=Client.KLINE_INTERVAL_30MINUTE)
        xrp30.div_bar_alligator_angularation()

        xrp1h = AlligatorExperiment({'XRP': currency1_balance, 'USDT': currency2_balance}, time_interval=Client.KLINE_INTERVAL_1HOUR)
        xrp1h.div_bar_alligator_angularation()

        xrp2h = AlligatorExperiment({'XRP': currency1_balance, 'USDT': currency2_balance}, time_interval=Client.KLINE_INTERVAL_2HOUR)
        xrp2h.div_bar_alligator_angularation()

# measure script run time
start_time = time.time()

x = TableAnalyzer()
#x.run_experiments_from_instance_list()

#x.instance_runner_manual()
x.tables_summary()

# measure script run time
print('Total running time', time.time() - start_time, 'sec.')