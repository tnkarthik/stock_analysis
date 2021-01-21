import sys
sys.path.append("..")

import matplotlib.pyplot as plt

import numpy as np
import pandas as pd

#from ..read_data import stock


def correlation(stock1, stock2, value = "Close"):
    """Function to plot stock price correlation b/w two stocks

    Parameters
    ----------
    stock1 : stock
        First stock
    stock2 : stock
        Second stock
    value : str
        Stock Price to use "Open"/"High"/"Low"/"Close"

    Returns
    -------
    None


    """

    ####
    if not (stock1.ohlc_data.empty or stock2.ohlc_data.empty):
        plt.clf()
        x, y = stock1.ohlc_data[value].iloc[:100], stock2.ohlc_data[value].iloc[:100]
        coeff = np.polyfit(x, y, deg = 1)
        plt.plot(x, y, ".")
        plt.plot(x, coeff[0]*x + coeff[1], "-")
        print("beta b/w {0} and {1} is {2}".format(stock2.symbol, stock1.symbol, coeff[0]))
        plt.show()
    else:
        print("Atleast one of the stocks {0}, {1} have no OHLC data available. \
               Cannot plot correlation".format(stock1.symbol, stock2.symbol))

def time_series(stock, value = "Close"):
    """Plot stock price time series

    Parameters
    ----------
    stock : stock
        Stock to plot
    value : type
        Stock price to use "Open"/"High"/"Low"/"Close"

    Returns
    -------
    None


    """

    if not stock.ohlc_data.empty:
        plt.clf()
        x = stock.ohlc_data.index
        y = stock.ohlc_data[value]
        plt.plot(x, y)
        plt.show()
