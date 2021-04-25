import yfinance as yf
import bs4 as bs
import requests
import pandas as pd

# Gets Yahoo Finance information for individual stock
def get_info(ticker):
    tickerDict = {}
    info = yf.Ticker(ticker)
    tickerDict['info'] = info.info
    tickerDict['history'] = info.history(period='max')    
    tickerDict['financials'] = info.financials
    tickerDict['balance_sheet'] = info.balance_sheet
    tickerDict['cashflow'] = info.cashflow
    
    return tickerDict

# Gets a list of every ticker in the S&P 500
def get_sp500_tickers():
    resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class':'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker[0:-1])

    return tickers

# Gets Yahoo Finance information for every ticker in the S&P 500.  Warning: takes roughly half an hour to complete
def get_sp500_info():
    tickers = get_sp500_tickers()
    sp500_dict = {}
    for ticker in tickers:
        sp500_dict[ticker] = get_info(ticker)

    return sp500_dict