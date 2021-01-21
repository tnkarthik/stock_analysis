import sys
sys.path.append("./src")

from src.read_data import stock
from src import plotting
#from plot import *

data_path = "./data/test_data"


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
    stocks = [stock(symbol, data_path) for symbol in list_of_stock_symbols]
    print(list_of_stock_symbols)

    #### Plot stock correlations
    for stock1 in stocks:
        for stock2 in stocks:
            if stock1 != stock2:
                plotting.correlation(stock1, stock2, "Close")

    for stock_i in stocks:
        pass
        #plotting.time_series(stock_i, "Open")


if __name__ == "__main__":
    stock_analysis(["AAPL", "GOOG", "MSFT", "FB"])
