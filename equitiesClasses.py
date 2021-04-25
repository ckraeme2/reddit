from equitiesScanner import get_info, get_sp500_info

# Class to store and obtain data for individual stock.  Exclusively uses get methods because new daily data will be obtained automatically through get_info call to Yahoo API
class Stock(object):

    def __init__(self, name):
        self.name = name
        self.info = get_info(name)
    
    def get_general_info():
        return self.info['info']

    def get_history(start=0):
        return self.info['history'][start:]

    def get_financials():
        return self.info['financials']
    
    def get_balance_sheet():
        return self.info['balance_sheet']

    def get_cashflow():
        return self.info['cashflow']

# Class to store and manipulate information on various stocks.  Also mainly uses get, with methods added to add stocks to and remove stocks from the database
class StockDatabase():

    # Initializes to contain all stocks within the S&P 500.  Probably want to change this unless get_sp500_info() runtime can be lowered
    def __init__():
        self.db = get_sp500_info()
    
    def add_stock(ticker):
        self.db[ticker] = get_info(ticker)
    
    def del_stock(ticker):
        del self.db[ticker]

    def get_stock(ticker):
        stock = Stock(ticker)

        return stock
    
    def get_general_info(ticker):
        return self.db[ticker]['info']

    def get_history(ticker, start=0):
        return self.db[ticker]['history'][start:]
    
    def get_financials(ticker):
        return self.db[ticker]['financials']

    def get_balance_sheet(ticker):
        return self.db[ticker]['balance_sheet']
    
    def get_cashflow(ticker):
        return self.db[ticker]['cashflow']
    
    def get_present_tickers():
        return self.db.keys()
    