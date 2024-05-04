import os
import sys

import sqlite3
import numpy as np
import pandas as pd

class data_factor:
    def __init__(self):
        self.start_date = '20'
        self.eval_date = '20240501'
        print("main dir is : ", os.getcwd())
        os.chdir(os.path.join(os.getcwd(), 'data'))
        print("data dir is : ", os.getcwd())

    def get_bond_data(self):
        # creating file path
        dbfile = 'TRACE.db'
        # Create a SQL connection to our SQLite database
        conn = sqlite3.connect(dbfile)

        # creating cursor
        cursor = conn.cursor()

        # reading all table names
        table_list = [a for a in cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table'")]

        # Fetching data from master_corp_agency
        query = """select * from master_corp_agency table
            master_corp_agency 
            where cusip_id in 
            (select distinct(cusip_id) as uniq_cusip from daily_btds)
            ;"""
        df=(cursor.execute(query)).fetchall()
        column_headers = [description[0] for description in cursor.description]
        master=pd.DataFrame(df,columns=column_headers)

        # Fetching data from daily_btds table
        query = "SELECT * FROM daily_btds"
        df=(cursor.execute(query)).fetchall()
        column_headers = [description[0] for description in cursor.description]
        df_btds=pd.DataFrame(df,columns=column_headers)

        # Calculating monthly coupon
        master['monthly_cpn']=master['cpn_rt']/12

        # Filtering for Investment Grade Bonds
        master_inv=master.loc[master['grade']=='I']

        merged_df=df_btds.merge(master_inv,on='cusip_id')

        # Adding Coupon to close price
        merged_df['close_pr']=merged_df['close_pr']+merged_df['monthly_cpn']

        bond_prices=merged_df[['trans_dt','cusip_id','close_pr']]
        # Convert trans_dt to datetime
        bond_prices['trans_dt'] = pd.to_datetime(bond_prices['trans_dt'])

        # Ensure data is sorted
        bond_prices = bond_prices.sort_values(by=['cusip_id', 'trans_dt'])

        # Remove duplicates by taking the mean or last (here we use mean for example)
        bond_prices = bond_prices.groupby(['trans_dt', 'cusip_id']).mean().reset_index()

        # Set the index to trans_dt
        bond_prices.set_index('trans_dt', inplace=True)

        # Find the min and max dates to create a full date range
        min_date = bond_prices.index.min()
        max_date = bond_prices.index.max()
        date_range = pd.date_range(min_date, max_date, freq='D')

        # Reindex the dataframe for each cusip_id to include all days in the range
        # and forward fill the missing data
        bond_prices = (
            bond_prices
            .groupby('cusip_id')
            .apply(lambda x: x.reindex(date_range).ffill().reset_index())
            .reset_index(drop=True)
        )

        # Rename 'index' back to 'trans_dt'
        bond_prices.rename(columns={'index': 'trans_dt'}, inplace=True)

        # Calculate log returns
        bond_prices['log_returns'] = np.log(bond_prices['close_pr'] / bond_prices['close_pr'].shift(1))

        # Average log returns by cusip_id
        # average_log_returns = bond_prices.groupby('cusip_id')['log_returns'].mean().reset_index()

        # Calculate monthly log returns
        bond_prices['month_year'] = bond_prices['trans_dt'].dt.to_period('M')
        monthly_log_returns = bond_prices.groupby(['cusip_id', 'month_year'])['log_returns'].sum().reset_index()


        return monthly_log_returns
    
    def run(self):
        self.get_factor_data()

# if __init__=="__main__":
#     data_bond.get_bond_data()