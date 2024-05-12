import os
import sys
import warnings
warnings.filterwarnings("ignore")

import yfinance as yf
import pandas as pd

# Define the tickers and the date range
tickers = ['AGG', 'IGSB', 'LQD', 'HYG', 'SHYG']
start_date = '2013-12-31'
end_date = '2023-12-31'

class data_etf:
    def __init__(self):
        # Define the tickers and the date range
        tickers = ['AGG', 'IGSB', 'LQD', 'HYG', 'SHYG']
        start_date = '2013-12-31'
        end_date = '2023-12-31'


        # Initialize an empty DataFrame for all tickers
        self.all_data = self.run()
        self.all_data.to_csv('etf_data_result.csv')

    # Function to download and process data for a single ticker
    def process_ticker_data(self, ticker):
        # Download the historical data
        data = yf.download(ticker, start=start_date, end=end_date, progress=False)
        
        # Resample to monthly frequency, using the last available data of the month
        monthly_data = data['Adj Close'].resample('M').last()
        
        # Calculate monthly returns
        monthly_returns = monthly_data.pct_change().fillna(0)
        
        # Calculate cumulative returns
        cumulative_returns = (1 + monthly_returns).cumprod() - 1
        
        # Prepare the DataFrame to return
        return pd.DataFrame({
            f'{ticker}_Adjusted_Return': monthly_returns,
            f'{ticker}_Cumulative_Return': cumulative_returns
        })
    
    def run(self):
        all_data = pd.DataFrame()
        # Loop through each ticker, process the data, and join with the main DataFrame
        for ticker in tickers:
            ticker_data = self.process_ticker_data(ticker)
            all_data = pd.concat([all_data, ticker_data], axis=1)
        print(all_data)
        return all_data

if __name__ == '__main__':
    run = data_etf()
