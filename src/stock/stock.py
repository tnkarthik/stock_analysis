import pandas as pd
import os
import yfinance as yf

class stock():
    """Basic stock class.

    Parameters
    ----------
    symbol : str
        Stock Ticker Symbol.
    data_path : type
        File path containing stock data.

    Attributes
    ----------
    ohlc_data : pandas.DataFrame
        Stock's daily Open/High/Low/Close price data.
    stats : dictionary
        mean and stdev stock price data.
    symbol

    """

    def __init__(self, symbol, period = '1mo'):
        self.symbol = symbol
        self.ohlc_data = self.get_stock_data(period = period) #self.read_stock_data(data_path)
        self.stats = {}
        self.stats = self.generate_summary_stats(time_period_in_days = self.ohlc_data.shape[0])

    def get_stock_data(self, period = "1mo"):
        """Function to get stock data using the yfinance app.

        Parameters
        ----------
        period : str
            Time period to get stock data for.

        Returns
        -------
        pandas DataFrame
            pandas DataFrame with OHLC, Volume, dividend, stock split data

        """
        data = yf.Ticker(self.symbol).history(period = period)
        return data

    def read_stock_data(self, data_path):
        """Method to read in stock OHLC price data from txt file.

        Parameters
        ----------
        data_path : str
            File path containing stock data.

        Returns
        -------
        pandas.DataFrame
            Stock OHLC data.

        """
        try:
            filepath = os.path.join(data_path, "{0}.us.txt".\
                                                 format(self.symbol.lower()))
            data = pd.read_csv(filepath)
            data = data.set_index("Date")

        except FileNotFoundError:
            print("{0} stock data not available".format(self.symbol))
            print(filepath)
            return pd.DataFrame()
        return data


    def generate_summary_stats(self, time_period_in_days):
        """Method to generate stock mean and stdev stats.

        Parameters
        ----------
        time_period_in_days : int
            Time period for generating stats.

        Returns
        -------
        tuple
            mean, stdev of the stock over the last "time_period_in_days" days.

        """
        if time_period_in_days > len(self.ohlc_data.index):
            time_period_in_days = len(self.ohlc_data.index)
            print("{0} days data is not available. Max available data is for \
                   {1} days".format(time_period_in_days, self.ohlc_data.index))

        if not self.stats.get(time_period_in_days, []):
            temp = self.ohlc_data.iloc[-time_period_in_days]["Close"]
            self.stats[time_period_in_days] = (temp.mean(), temp.std())

        return self.stats[time_period_in_days]


    def simple_moving_avg(self, time_period_in_days = 5):
        """Method to generate simple moving average of stock price data.

        Parameters
        ----------
        time_period_in_days : int
            time window in days to use for average stock price

        Returns
        -------
        pandas.DataFrame
            Simple moving averaged stock price data

        """
        return self.ohlc_data.rolling("{0}D".format(time_period_in_days)).mean()

    def exp_moving_avg(self, alpha = 0.1):
        """Method to generate Exponential Moving Average of stock price data

        Parameters
        ----------
        alpha : float
            alpha parameter of the exponetial moving average function

        Returns
        -------
        pandas.DataFrame
            Exponential Moving Average stock price data

        """
        return self.ohlc_data.ewm(alpha = alpha).mean()


    def bollinger_bands(self, time_period_in_days = 20):
        """Function to calculate Bollinger Bands.

        Parameters
        ----------
        time_period_in_days : int
            Number of days to calculate avg and stdev.

        Returns
        -------
        tuple
            Tuple of pandas DataFrame objects containing Bollinger Band data

        """
        data = self.ohlc_data
        period = min(time_period_in_days, self.ohlc_data.shape[0])
        typical_price = (data['Close'] + data['High'] + data['Low'])/3.0
        rolling = typical_price.rolling("{0}D".format(period))
        sma = rolling.mean()
        stdev = rolling.std()
        BOLU = sma + 2.0*stdev
        BOLD = sma - 2.0*stdev
        return BOLU, BOLD


    def technicals(self,):
        pass
