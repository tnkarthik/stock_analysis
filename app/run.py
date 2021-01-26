import json
import plotly
import pandas as pd

from flask import Flask
from flask import render_template, request, jsonify
from plotly.graph_objs import Bar, Histogram, Scatter, Table
import plotly.graph_objs as go
import yfinance as yf

import sys
import re
import datetime as dt
import sys

sys.path.append("..")

from src.stock import stock
from src.plotting import basic_plots

app = Flask(__name__)


# index webpage displays cool visuals and receives user input text for model
@app.route('/')
@app.route('/index')
def index():
    ticker = 'AAPL'
    period = '1y'
    graphs = basic_plots(ticker, period)

    # encode plotly graphs in JSON
    ids = ["graph-{}".format(i) for i, _ in enumerate(graphs)]
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    # render web page with plotly graphs
    return render_template('master.html', ids=ids, graphJSON=graphJSON)


# web page that handles user query and displays model results
@app.route('/go')
def go():
    # save user input in query
    ticker = request.args.get('query', '')
    period = '1y'
    graphs = basic_plots(ticker, period)

    # encode plotly graphs in JSON
    ids = ["graph-{}".format(i) for i, _ in enumerate(graphs)]
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

# This will render the go.html Please see that file.
    return render_template(
        'go.html',
        query=ticker, ids=ids, graphJSON=graphJSON)


def main():
    app.run(host='127.0.0.1', port=3001, debug=True)


if __name__ == '__main__':
    main()
