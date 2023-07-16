from flask import Flask, jsonify, render_template, request
from account import Account
from StockContainer import StockContainer
import os
from dotenv import load_dotenv
import shutil
import glob
from Backtester import Backtester
from MACDStrategy import MACD_Strategy
stock_list = []

app = Flask(__name__)

load_dotenv()

stock_list = []

app.config['account'] = Account(os.getenv('API_KEY'), os.getenv('SECRET_KEY'), base_url='https://paper-api.alpaca.markets')

app.config['main'] = StockContainer(app.config['account'], stock_list)
    
# Used for the Dropdown.js    
@app.route('/api/stocks/symbol')
def get_stocks_symbol():
    active_assets = app.config['account'].api.list_assets(status='active') 
    symbols = []
    for asset in active_assets:
        symbols.append(asset.symbol)
    return jsonify(symbols)

@app.route('/api/stocks/name')
def get_stocks_name():
    active_assets = app.config['account'].api.list_assets(status='active') 
    names = []
    for asset in active_assets:
        names.append(asset.name)
    return jsonify(names)


@app.route('/api/stocks')
def get_stocks():
    active_assets = app.config['account'].api.list_assets(status='active') 
    stocks = {}
    for asset in active_assets:
        stocks.update({asset.symbol : asset.name})

    return jsonify(stocks)

@app.route('/api/stocks/add', methods = ['POST'])
def add_stock():
    data = request.get_json()
    selected_stock = data.get('selectedValue')
    check = app.config['main'].add_stock(selected_stock)

    name = app.config['main'].account.get_stock_name(selected_stock)

    if check is True:
        response = {'message': name + ' has been added'}
    else:
        response = {'message': name + ' has been not been added as it does not profit'}
  

    return jsonify(response)


@app.route('/api/stocks/remove', methods = ['POST'])
def remove_stock():
    data = request.get_json()
    selected_stock = data.get('selectedValue')

    app.config['main'].remove_stock(selected_stock)


    name = app.config['main'].account.get_stock_name(selected_stock)

    response = {'message': name + ' has been removed'}
    return jsonify(response)

@app.route('/api/stocks/stat', methods = ["POST"]) # For single stock
def stat():
    data = request.get_json()
    selected_stock = data

    stock = MACD_Strategy(app.config['account'], selected_stock)

    tester = Backtester([stock])

    tester.execute()
    if len(tester.remove_stocks) != 0:
        winrate = 0
        money_made = 0
    else:
        winrate = tester.winrates[0]
        money_made = tester.money_made[0]

    response = {'winrate': winrate,
                'money' : money_made}
    
    return jsonify(response)

# Used for Stats.js
@app.route('/api/stocks/stats') 
def stats():
    if len(app.config['main'].MACD_objects) == 0:
        response = {'message':'There are currently no objects'}
        return jsonify(response)

    data = app.config['main'].get_stats()

    return jsonify(data)

@app.route('/api/stocks/stat/average') 
def stats_average():
    if len(app.config['main'].MACD_objects) == 0:
        response = {'message':'There are currently no objects'}
        return jsonify(response)

    data = app.config['main'].average_stats()

    return jsonify(data)

# Used for Plot.js
@app.route('/api/plot/filenames')
def get_images():
    if len(app.config['main'].stocks) == 0:
        return jsonify({'error': 'There is are currently 0 stocks'})
    
    image_directory = 'plots'  # Replace with the actual image directory path
    image_list = []

    for filename in os.listdir(image_directory):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            image_url = f'/{filename}'
            image_list.append(image_url)

    return jsonify(image_list)

@app.route('/api/plot/generate')
def generate_plots():

    source_directory = 'C:\\Users\\Steve\\Documents\\Trading Bot React App\\flask-server\\plots'
    public_directory = "C:\\Users\\Steve\\Documents\\Trading Bot React App\\client\\public"

    os.chdir(public_directory)
    plot_folder = 'plots'
    if not os.path.exists(plot_folder):
        os.makedirs(plot_folder)
    else:
        # Delete previous plot files
        files = glob.glob(os.path.join(plot_folder, '*.png'))
        for file in files:
            os.remove(file)
    
    if len(app.config['main'].stocks) == 0:
        return jsonify({'error': 'There is are currently 0 stocks'})





    app.config['main'].make_plots()

    public_directory = "C:\\Users\\Steve\\Documents\\Trading Bot React App\\client\\public\\plots"

    # Iterate over the files in the source directory
    for filename in os.listdir(source_directory):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            source_path = os.path.join(source_directory, filename)
            destination_path = os.path.join(public_directory, filename)

            # Copy the file to the public directory
            shutil.copy(source_path, destination_path)
    return jsonify({'message': 'Plots generated successfully'})


# Used for Execute.js
@app.route('/api/execute')
def execute():
    if len(app.config['main'].MACD_objects) == 0:
        response = {'message': 'There is currently no stocks chosen'}
        return jsonify(response)
    data = app.config['main'].execute()
    
    return jsonify(data)




if __name__ == "__main__":
    app.run("localhost", port = 5000, debug=True)

    
