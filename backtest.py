from pylab import mpl
mpl.rcParams['font.sans-serif']=['SimHei']
import pandas as pd
from datetime import datetime
import backtrader as bt
from backtrader_plotting import Bokeh
from backtrader_plotting.schemes import Tradimo
from binance.client import Client

apikey = ''
secret = ''

client= Client(,)

historical = client.get_historical_klines('BTCUSDT','1d' ,'2022-12-16')
hist_df=pd.DataFrame(historical)
hist_df.columns = ['date','open','high','low','close','volume','Close Time','Quote Assets Volume','Number of Trades','Taker Buy Base Asset Volume','Taker Buy Quote Asset Volume','Ignore']
dataframe=pd.DataFrame(hist_df, columns=['date','open','high','low','close','volume'])
dataframe['date'] = pd.to_datetime(dataframe['date']/1000,unit='s')
numeric_colunms=['open','high','low','close','volume']
dataframe[numeric_colunms] = dataframe[numeric_colunms].apply(pd.to_numeric,axis=1)
dataframe.index=pd.to_datetime(dataframe.date)
dataframe=dataframe[['open','high','low','close','volume']]
dataframe['openinterest'] = 0

class my_strategy1(bt.Strategy):

    params=(
        ('maperiod',20),
           )

    def __init__(self):
        self.dataclose=self.datas[0].close
        # 初始化交易指令、买卖价格和手续费
        self.order = None
        self.buyprice = None
        self.buycomm = None

        self.sma = bt.indicators.SimpleMovingAverage(
                      self.datas[0], period=self.params.maperiod)

    def next(self):
        if self.order:
            return
        if not self.position: # 没有持仓
            if self.dataclose[0] > self.sma[0]:
                #执行买入
                self.order = self.buy(size=50)
        else:
            if self.dataclose[0] < self.sma[0]:
                #执行卖出
                self.order = self.sell(size=100)

    def log(self, txt, dt=None):

        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'买入:\n价格:{order.executed.price},\
                成本:{order.executed.value},\
                手续费:{order.executed.comm}')
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:
                self.log(f'卖出:\n价格：{order.executed.price},\
                成本: {order.executed.value},\
                手续费{order.executed.comm}')
            self.bar_executed = len(self)

        # 如果指令取消/交易失败, 报告结果
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('交易失败')
        self.order = None



if __name__ == "__main__":

    #回测期间
    start=datetime(2022,12,16)
    end=datetime(2022,12,18)

    # 加载数据
    data = bt.feeds.PandasData(dataname=dataframe,fromdate=start,todate=end)

    # 初始化cerebro回测系统设置
    cerebro = bt.Cerebro()

    #将数据传入回测系统
    cerebro.adddata(data,name=12344)

    # 将交易策略加载到回测系统中
    cerebro.addstrategy(my_strategy1)

    # 设置初始资本为10,000
    startcash = 100000000
    cerebro.broker.setcash(startcash)

    # 设置交易手续费为 0.2%
    cerebro.broker.setcommission(commission= 0.003)

    d1=start.strftime('%Y%m%d')
    d2=end.strftime('%Y%m%d')
    print(f'初始资金: {startcash}\n回测期间：{d1}:{d2}')

    #运行回测系统
    cerebro.run()
    #获取回测结束后的总资金
    portvalue = cerebro.broker.getvalue()
    pnl = portvalue - startcash
    #打印结果
    print(f'总资金: {round(portvalue,2)}')

    b = Bokeh(style='bar', plot_mode='single', scheme=Tradimo())
    cerebro.plot(b)