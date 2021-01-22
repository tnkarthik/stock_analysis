import sys
sys.path.append("./src")

from src.read_data import stock
from src import plotting
import matplotlib.pyplot as plt
import plotly.graph_objects as go
#from plot import *

#data_path = "./data/test_data"


def stock_analysis(list_of_stock_symbols):
    """Main stock analysis function to define stock analysis operations

    Parameters
    ----------
    list_of_stock_symbols : list
        List of stock ticker symbols.

    Returns
    -------
    None


    """
    #### Read the stock data
    stocks = [stock(symbol, period = "1y") for symbol in list_of_stock_symbols]
    print(list_of_stock_symbols)

    #### Plot stock correlations
    #for stock1 in stocks:
    #    for stock2 in stocks:
    #        if stock1 != stock2:
    #            plotting.correlation(stock1, stock2, "Close")

    data = []
    for stock_i in stocks:
        data_i = go.Scatter(x = stock_i.ohlc_data.index , \
                            y = stock_i.ohlc_data['Close'], mode = 'markers', \
                            name = stock_i.symbol)

        data_i1 = go.Scatter(x = stock_i.ohlc_data.index , \
                            y = stock_i.simple_moving_avg()['Close'], \
                            mode = 'lines', name = stock_i.symbol)
        data.append(data_i)
        data.append(data_i1)
    fig = go.Figure(data = data, layout = go.Layout(height = 600, width = 800))
    #fig.show()


if __name__ == "__main__":
    stock_analysis(["AAPL", "GOOG", "MSFT", "FB"])
