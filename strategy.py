from freqtrade.strategy import IStrategy, IntParameter
import talib.abstract as ta

class MobileStrategy(IStrategy):
    timeframe = '15m'
    minimal_roi = {"0": 0.02, "60": 0.01, "120": 0}
    stoploss = -0.05
    trailing_stop = True
    trailing_stop_positive = 0.01
    trailing_stop_positive_offset = 0.02

    rsi_buy = IntParameter(25, 40, default=30, space='buy')
    rsi_sell = IntParameter(70, 85, default=75, space='sell')
    ema_short = IntParameter(10, 30, default=20, space='buy')
    ema_long = IntParameter(40, 80, default=50, space='buy')

    def populate_indicators(self, dataframe, metadata):
        dataframe['ema_short'] = ta.EMA(dataframe, timeperiod=self.ema_short.value)
        dataframe['ema_long'] = ta.EMA(dataframe, timeperiod=self.ema_long.value)
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)
        return dataframe

    def populate_buy_trend(self, dataframe, metadata):
        dataframe.loc[
            (dataframe['rsi'] < self.rsi_buy.value) &
            (dataframe['ema_short'] > dataframe['ema_long']),
            'buy'] = 1
        return dataframe

    def populate_sell_trend(self, dataframe, metadata):
        dataframe.loc[
            (dataframe['rsi'] > self.rsi_sell.value) |
            (dataframe['ema_short'] < dataframe['ema_long']),
            'sell'] = 1
        return dataframe
