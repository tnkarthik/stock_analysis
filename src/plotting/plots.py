import sys
import datetime as dt
sys.path.append("..")

import matplotlib.pyplot as plt

import numpy as np
import pandas as pd

from plotly.graph_objs import Scatter, Table
from src.stock import stock

def trace(x, y, name, mode, line_color, fill = None, fillcolor = None):
    trace = \
            Scatter(
                x = x,
                y = y,
                mode = mode,
                name = name,
                line_color = line_color,
                fill = fill,
                fillcolor = fillcolor
            )
    return trace


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

    summary_cols = ['Open', 'High', 'Low', 'Close']
    data_summary = stock_info.ohlc_data[summary_cols].\
                    agg([np.mean, np.std, np.max, np.min])

    #### Define traces and layout for Scatter plot
    trace_stock = trace(data.index, data['Close'], ticker, 'markers', 'green')
    trace_ewma =  trace(data_ewm.index, data_ewm['Close'], 'EWMA', 'lines', 'green')
    trace_bold =  trace(bold.index, bold.values, 'Lower Bollinger Band', 'lines', 'orange')
    trace_bolu =  trace(bolu.index, bolu.values, 'Upper Bollinger Band', \
                        'lines', 'orange', 'tonexty', 'rgba(0,255,0,0.4)')

    layout_scatter = \
                    {
                        'title': '{0} stock performance'.format(ticker),
                        'yaxis':
                        {
                            'title': "Stock Value"
                        },
                        'xaxis':
                        {
                            'title': "DateTime"
                        }
                    }


    #### Define tables and layout for summary/data tables
    table_summary = \
            Table(
                header=dict(values = [''] + data_summary.columns.tolist(), \
                            fill = dict(color = 'paleturquoise')),
                cells=dict(values = \
                           [['mean', 'stdev', 'max', 'min']] + \
                           [data_summary[col].apply(lambda x: round(x,2)) \
                                            for col in data_summary.columns]),
            )

    table_data = \
            Table(
                header=dict(values = ['DateTime'] + data.columns.tolist(), \
                            fill = dict(color = 'paleturquoise')),
                cells=dict(values = \
                           [[dt.datetime.strftime(x, "%m-%d-%Y") for x in data.index]] + \
                           [data[col].apply(lambda x: round(x,2)) \
                                            for col in data.columns]),
            )

    #### Create a list of all graph objects to be displayed
    graphs = [
        {
            'data': [trace_stock, trace_ewma, trace_bold, trace_bolu],
            'layout': layout_scatter
        },

        {
            'data': [table_summary],
            'layout':
            {
                'title': '{0} Stock Data Summary'.format(ticker)
            }
        },

        {
            'data': [table_data],
            'layout':
            {
                'title': '{0} Stock Data'.format(ticker)
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
