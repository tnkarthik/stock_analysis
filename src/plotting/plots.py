import sys
import datetime as dt
sys.path.append("..")

import matplotlib.pyplot as plt

import numpy as np
import pandas as pd

from plotly.graph_objs import Scatter, Table
from src.stock import stock


def basic_plots(ticker, period = '1y'):
    """Function to generate basic stock plots.

    Parameters
    ----------
    ticker : str
        Stock Ticker Symbol.
    period : str
        Time period to display data for.

    Returns
    -------
    list
        list of plotly.graph_objs.

    """
    stock_info = stock(ticker, period)
    data = stock_info.ohlc_data
    bolu, bold = stock_info.bollinger_bands(time_period_in_days = 20)
    data_ewm = stock_info.exp_moving_avg(alpha = 0.2)

    graphs = [
        {
            'data': [
                Scatter(
                    x=data.index,
                    y=data['Close'],
                    name = "{0} closing price".format(ticker),
                    mode = 'markers',
                    marker_color = 'green'
                ),

                Scatter(
                    x = data_ewm.index,
                    y = data_ewm['Close'],
                    name = 'EWMA',
                    mode = 'lines',
                    line_color = 'green'
                ),

                Scatter(
                    x = bold.index,
                    y = bold.values,
                    mode = 'lines',
                    name = 'lower bollinger band',
                    line_color = 'orange'
                ),

                Scatter(
                    x = bolu.index,
                    y = bolu.values,
                    mode = 'lines',
                    fill = 'tonexty',
                    name = 'upper bollinger band',
                    line_color = 'orange',
                    fillcolor = 'rgba(0,255,0,0.4)'
                )
            ],

            'layout': {
                'title': '{0} stock performance'.format(ticker),
                'yaxis': {
                    'title': "Stock Value"
                },
                'xaxis': {
                    'title': "DateTime"
                }
            }
        },

        {
            'data': [
                Table(
                    header=dict(values = ['DateTime'] + data.columns.tolist(), \
                                fill = dict(color = 'paleturquoise')),
                    cells=dict(values = \
                               [[dt.datetime.strftime(x, "%m-%d-%Y") for x in data.index]] + \
                               [data[col].apply(lambda x: round(x,2)) \
                                                for col in data.columns]),

                )
            ],

            'layout': {
                'title': '{0} Stock Data Summary'.format(ticker)
            }


        },


    ]

    return graphs

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
