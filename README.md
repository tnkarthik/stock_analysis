# stock_analysis

stock_analysis is a Python library for performing/plotting some common operations with stock data.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install stock_analysis
```

## Usage

```python
import stock_analysis
## Create a stock object
aapl = stock_analysis.stock(symbol = "AAPL", data_path = <path_to_file_with_stock_data>)


## Calculate key stats
## 100 day average and stdev
aapl.generate_summary_stats(time_period_in_days = 100)


## Retreive all previously calculated summary stats
print(aapl.stats) ## Print a dict of all stats
print(aapl.stats[100]) ## Print 100 day stats

## Plot stock price vs. time
stock_analysis.time_series(aapl_stock, value = "Close", \
                           types = ["raw", "simple_moving_avg", "exp_moving_avg"])

## Plot correlation b/w two stocks
aapl = stock_analysis.stock("AAPL", data_path = <path_to_file_with_stock_data>)
msft = stock_analysis.stock("MSFT", data_path = <path_to_file_with_stock_data>)
stock_analysis.correlation(aapl, msft, "Close")

```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
