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

app = Flask(__name__)


# index webpage displays cool visuals and receives user input text for model
@app.route('/')
@app.route('/index')
def index():
    aapl = stock('AAPL', period = '1y')
    data = aapl.ohlc_data#yf.Ticker('AAPL').history(period = '1mo')

    graphs = [
        {
            'data': [
                Scatter(
                    x=data.index,
                    y=data['Close']
                )
            ],

            'layout': {
                'title': 'AAPL stock performance',
                'yaxis': {
                    'title': "Stock Value"
                },
                'xaxis': {
                    'title': "DateTime"
                }
            }
        }

    ]

    # encode plotly graphs in JSON
    ids = ["graph-{}".format(i) for i, _ in enumerate(graphs)]
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    # render web page with plotly graphs
    return render_template('master.html', ids=ids, graphJSON=graphJSON)


# web page that handles user query and displays model results
@app.route('/go')
def go():
    # save user input in query
    query = request.args.get('query', '')

    stock_query = stock(query, period = '1y')
    data = stock_query.ohlc_data#yf.Ticker(query).history(period = '1y')

    graphs = [
        {
            'data': [
                Scatter(
                    x=data.index,
                    y=data['Close'],
                    mode = 'markers',
                    name = query
                ),

                Scatter(
                    x = data.index,
                    y = data.ewm(alpha = 0.2).mean()['Close'],
                    mode = 'lines',
                    name = 'EWMA alpha = {0}'.format(0.2)
                ),

                Scatter(
                    x = data.index,
                    y = data.rolling("5D").mean()['Close'],
                    mode = 'lines',
                    name = 'SMA period: {0}'.format("5D")
                )
            ],

            'layout': {
                'title': '{0} stock performance'.format(query),
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


        },


    ]

    # encode plotly graphs in JSON
    ids = ["graph-{}".format(i) for i, _ in enumerate(graphs)]
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)




# This will render the go.html Please see that file.
    return render_template(
        'go.html',
        query=query, ids=ids, graphJSON=graphJSON)


def main():
    app.run(host='127.0.0.1', port=3001, debug=True)


if __name__ == '__main__':
    main()
