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

app = Flask(__name__)


# index webpage displays cool visuals and receives user input text for model
@app.route('/')
@app.route('/index')
def index():
    aapl = yf.Ticker('AAPL').history(period = '1mo')

    graphs = [
        {
            'data': [
                Scatter(
                    x=aapl.index,
                    y=aapl['Close']
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

    stock = yf.Ticker(query).history(period = '1y')

    graphs = [
        {
            'data': [
                Scatter(
                    x=stock.index,
                    y=stock['Close'],
                    mode = 'markers',
                    name = query
                ),

                Scatter(
                    x = stock.index,
                    y = stock.ewm(alpha = 0.2).mean()['Close'],
                    mode = 'lines',
                    name = query
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
                    header=dict(values = ['DateTime'] + stock.columns.tolist(), \
                                fill = dict(color = 'paleturquoise')),
                    cells=dict(values = \
                               [[dt.datetime.strftime(x, "%m-%d-%Y") for x in stock.index]] + \
                               [stock[col].apply(lambda x: round(x,2)) \
                                                for col in stock.columns]),

                )
            ],


        }
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
