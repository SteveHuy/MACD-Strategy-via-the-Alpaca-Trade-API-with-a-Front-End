from account import Account
from MACDStrategy import MACD_Strategy
from Backtester import Backtester
import os
import uuid
import glob
import matplotlib.pyplot as plt

class StockContainer:
    def __init__(self, account: Account, stocks: list[str]):
        """
        Initializes a StockContainer object.

        Args:
            account (Account): An instance of the Account class.
            stocks (list[str]): A list of stock symbols.
        """
        self.account = account
        self.stocks = stocks
        self.MACD_objects = []
        self.make_MACD_objects()
        self.backtester = Backtester(self.MACD_objects)
        if len(self.MACD_objects) != 0:
            self.execute_backtester()





    def execute_backtester(self):
        """
        Executes the backtester, removes stocks from the list if necessary,
        and sets the ratios.
        """
        self.backtester.execute()
        remove_stocks = self.backtester.remove_stocks
        for stock in remove_stocks:
            self.stocks.remove(stock.symbol)
        self.backtester.set_ratios()


    def make_MACD_objects(self):
        """
        Creates MACD_Strategy objects for each stock in the list.
        """
        self.MACD_objects = []
        for stock in self.stocks:
            self.MACD_objects.append(MACD_Strategy(self.account, stock))


    def execute(self):
        """
        Executes the backtester and MACD strategies.
        """
        self.backtester.execute()
        res = {}
        for MACD_object in self.MACD_objects:
            name = self.account.get_stock_name(MACD_object.symbol)
            res[name] = MACD_object.execute()

        return res

    def add_stock(self, stock: str):
        """
        Adds a stock to the list and creates a corresponding MACD strategy object.

        Args:
            stock (str): The stock symbol to add.
        """
        if stock in self.stocks:
            print(stock + " is already in the list")
            return False
        else:
            stock_macd = MACD_Strategy(self.account, stock)
            response = self.backtester.add_stock(stock_macd)
            if response is True:
                self.stocks.append(stock)
                self.MACD_objects.append(stock_macd)
                self.backtester.set_recent_ratio()
                print(stock + " has been added from the list")

                return True
            else:
                return False

            
        
    def get_stats(self):
        """
        Returns the stats of the backtester
        """
        data = []
        for i in range(len(self.MACD_objects)):
            stock = {
                "name":self.account.get_stock_name(self.stocks[i]),
                "symbol":self.stocks[i],
                "winrate":round(self.backtester.winrates[i] * 100, 2),
                "money_made":self.backtester.money_made[i],
                "profit_take":self.backtester.optimal_profit_ratio[i],
                "stop_loss":self.backtester.optimal_risk_ratio[i]
            }
            data.append(stock)
        return data


    def average_stats(self):
        """
        gets the average winrate and money made
        """
        money_made = sum(self.backtester.money_made)/len(self.backtester.money_made)
        winrate = sum(self.backtester.winrates)/len(self.backtester.winrates)

        data = {
            "money_made": round(money_made,2),
            "winrate": round(winrate,2)
        }

        return data
    
    def remove_stock(self, stock:str):
        """
        Removes a stock from the list and its corresponding MACD strategy object.

        Args:
            stock (str): The stock symbol to remove.
        """
        if stock in self.stocks:
            index = self.stocks.index(stock)
            self.stocks.remove(stock)
            self.MACD_objects.pop(index)
            print(stock + " has been removed from the list")
            return True
        else:
            print(stock + " is not in the list")
            return False

    def make_plots(self):
        if len(self.MACD_objects) == 0:
            return('There is currently no stocks')
        self.delete_previous_plots()
        for MACD in self.MACD_objects:
            MACD.plot_save()
            self.save_plot()
        return 

    def delete_previous_plots(self):
        # Create a folder to store plots if it doesn't exist
        plot_folder = 'plots'
        if not os.path.exists(plot_folder):
            os.makedirs(plot_folder)
        else:
            # Delete previous plot files
            files = glob.glob(os.path.join(plot_folder, '*.png'))
            for file in files:
                os.remove(file)
        return

    def save_plot(self):
        # Create a folder to store plots if it doesn't exist
        plot_folder = 'plots'
        if not os.path.exists(plot_folder):
            os.makedirs(plot_folder)

        # Generate a unique file name for each plot
        file_name = str(uuid.uuid4()) + '.png'
        file_path = os.path.join(plot_folder, file_name)

        # Save the plot as an image file
        plt.savefig(file_path, format='png')
        plt.close()  # Close the plot to free up resources
        return 