
import sqlite3
import pandas as pd
import numpy as np

import sqlite3

def fetch_data_from_sqlite(db_file, query):
    """
    Fetches data from a SQLite database using the provided SQL query.
    
    Parameters:
        db_file (str): Path to the SQLite database file.
        query (str): SQL query to execute.
        
    Returns:
        list of tuples: Fetched data.
    """
    try:
        # Connect to the SQLite database file
        conn = sqlite3.connect(db_file)
        
        cursor = conn.cursor()
        cursor.execute(query) # Execute the SQL query      
        rows = cursor.fetchall() # Fetch all rows from the result set

        # Close the cursor and connection
        cursor.close()
        conn.close()

        return rows
    
    except sqlite3.Error as e:
        print("Error fetching data from SQLite database:", e)
        return None



class FactorInvesting:
    def __init__(self, data):
        self.data = data


    def calculate_factors(self, fin_ratio):

        fin_ratio['profit_growth_rate'] = fin_ratio.groupby('cusip')['npm'].pct_change()

        # 2. Liquidity Ratio Dynamics

        equity_invcap_by_cusip = fin_ratio.groupby('cusip')['equity_invcap'].transform('mean')
        fin_ratio['cop_at'] = fin_ratio['opmbd']/ equity_invcap_by_cusip
        fin_ratio['noa_gr1a'] = fin_ratio.groupby('cusip')['roa'].diff() #  (Change in net operating assets)
        fin_ratio['saleq_gr1'] = fin_ratio.groupby('cusip')['sale_invcap'].pct_change() # (Sales growth (1 quarter))
        fin_ratio['curr_ratio_change'] = fin_ratio.groupby('cusip')['curr_ratio'].diff()
        fin_ratio['quick_ratio_change'] = fin_ratio.groupby('cusip')['quick_ratio'].diff()
        fin_ratio['cash_ratio_change'] = fin_ratio.groupby('cusip')['cash_ratio'].diff()

        # 3. Debt Management Efficiency

        # Calculate the mean of 'evm' column for each group
        evm_mean_by_cusip = fin_ratio.groupby('cusip')['evm'].transform('mean')
        # Calculate the ratio of 'totdebt_invcap' to the mean of 'evm' for each group
        fin_ratio['debt_me'] = fin_ratio['totdebt_invcap'] / evm_mean_by_cusip

        fin_ratio['debt_assets_change'] = fin_ratio.groupby('cusip')['debt_assets'].diff()
        fin_ratio['de_ratio_change'] = fin_ratio.groupby('cusip')['de_ratio'].diff()

        # 4. Capital Structure Stability
        fin_ratio['debt_capital_change'] = fin_ratio.groupby('cusip')['debt_capital'].diff()
        fin_ratio['debt_invcap_change'] = fin_ratio.groupby('cusip')['debt_invcap'].diff()

        # 5. Earnings Quality Metrics
        opmbd_by_cusip = fin_ratio.groupby('cusip')['opmbd'].transform('mean')
        fin_ratio['recurring_earnings_ratio'] = fin_ratio['opmad']/ opmbd_by_cusip
        fin_ratio['earnings_growth_consistency'] = fin_ratio.groupby('cusip')['pe_op_basic'].pct_change()

        # 6. Investment Efficiency Ratios
        fin_ratio['roce_change'] = fin_ratio.groupby('cusip')['roce'].diff()
        fin_ratio['aftret_invcapx_change'] = fin_ratio.groupby('cusip')['aftret_invcapx'].diff()

        # 7. Market Sentiment Indicators
        fin_ratio['ptb_change'] = fin_ratio.groupby('cusip')['ptb'].diff()
        fin_ratio['peg_trailing_change'] = fin_ratio.groupby('cusip')['PEG_trailing'].diff()

        # 8. Risk-adjusted Performance Measures
        fin_ratio['efftax_change'] = fin_ratio.groupby('cusip')['efftax'].diff()

        # 9. Operating capital Indicator 
        fin_ratio['cowc_gr1a'] = fin_ratio.groupby('cusip')['ocf_lct'].diff() # Change in current operating working capital
        fin_ratio['nncoa_gr1a'] = fin_ratio.groupby('cusip')['aftret_invcapx'].diff() # Change in net noncurrent operating assets
        
        fin_ratio['ocf_me'] = fin_ratio['ocf_lct'] / evm_mean_by_cusip # Operating cash flow-to-market

        return fin_ratio



# Example Usage:
if __name__ == "__main__":


    #db_file = 'your_database.db'
    #query = "SELECT * FROM your_table"
    #data = fetch_data_from_sqlite(db_file, query)
    #if data:
    #    for row in data:
    #        print(row)

    data = pd.read_csv('wrds_fin_ratio.csv')
    # Assume 'data' is a DataFrame containing historical financial data
    factor_investing = FactorInvesting(data)

    # Calculate various factors
    factor_results = factor_investing.calculate_factors(data)
    print(factor_results)
    #factor_results.to_csv('factor_results.csv')



