from flask import Flask, jsonify, request
import requests 
from account import Account
from StockContainer import StockContainer
import os
import io
import base64

app = Flask(__name__)

@app.route('/plot')
def plot():
    account = Account(os.getenv('API_KEY'), os.getenv('SECRET_KEY'), base_url='https://paper-api.alpaca.markets')
    stock_list = ['ABNB', 'ADP','AMZN' , 'TMUS', 'AAPL', 'TSLA', 'MSFT']
    main = StockContainer(account, stock_list)
    main.make_plots()
    plot_file = '/Documents/Trading Bot React App/plots'

    return jsonify({'plot_url': plot_file})


if __name__ == '__main__':
    app.run(debug=True)