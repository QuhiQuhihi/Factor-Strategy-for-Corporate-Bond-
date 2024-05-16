import os
import sys
import warnings
warnings.filterwarnings("ignore")

import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from base_model_ranking import rank_base_factor

class portfolio_base:
    def __init__(self):
        # Define the tickers and the date range
        self.start_date = '2013-12-31'
        self.end_date = '2023-12-31'

        # loading base_rank dataframe
        self.df_base_rank = rank_base_factor().run()
        self.df_base_rank['market_signal'] = 0
        self.df_base_rank['term_signal'] = 0

        self.month_year_base_rank = self.df_base_rank['month_year'].unique()
        print(self.month_year_base_rank)

        print("current dir is : ", os.getcwd())
        self.main_dir = os.path.join("C:\\", 'workspace', 'Factor-Strategy-for-Corporate-Bond-')
        print("main dir is : ", self.main_dir)
        self.data_dir = os.path.join(self.main_dir, "(Chapter1)Data")
        print("data dir is : ", self.data_dir)

    # Function to download and process data for a single ticker
    def load_liquid_bond_return(self, cusip_ids, month_year):
        os.chdir(self.data_dir)
        dbfile = 'TRACE.db'
        # Create a SQL connection to our SQLite database
        conn = sqlite3.connect(dbfile)
        print("{} is connected for {}".format(dbfile, "load_base_factor_data function"))
        # creating cursor
        cursor = conn.cursor()
        formatted_cusips = "'" + "', '".join(cusip_ids) + "'"

        query = """
            select month_year, cusip_id, log_returns
            from bond_returns
            where month_year = '{}' and cusip_id in ({})
        """.format(month_year,formatted_cusips)

        df=(cursor.execute(query)).fetchall()
        print("market factor is loaded")
        column_headers = [description[0] for description in cursor.description]
        df_base_bond_return=pd.DataFrame(df,columns=column_headers)
        print(df_base_bond_return)
        return df_base_bond_return

    def build_portfolio(self):
        
        # long market signal if rank is top 33%
        self.df_base_rank['market_signal'].apply((lambda x: 1 if x < 0.33 else x))
        # short market signal if rank is bottom 33%
        self.df_base_rank['market_signal'].apply((lambda x: -1 if x > 0.66 else x))

        # long term signal if rank is top 33%
        self.df_base_rank['term_signal'].apply((lambda x: 1 if x < 0.33 else x))
        # short term signal if rank is bottom 33%
        self.df_base_rank['term_signal'].apply((lambda x: -1 if x > 0.66 else x))

        ###  build 1/n long and short portfolio to check whether this strategy works 
        # self.df_base_portfolio_weight = pd.DataFrame()
        # for yyyy_mm in self.month_year_base_rank:
        #     monthly_rank = self.df_base_rank.query("month_year == '{}'".format(yyyy_mm))
        #     num_monthly_rank = monthly_rank.count()
        #     num_monthly_rank_long = monthly_rank.query("market_signal > {}".format(0.9)).count()
        #     num_monthly_rank_short = monthly_rank.query("market_signal < {}".format(-0.9)).count()
        #     num_monthly_rank_neutral = num_monthly_rank - num_monthly_rank_long - num_monthly_rank_short
            
        #     monthly_rank['weight'] 
        #     monthly_rank_market = monthly_rank.query("market_rank_percentile > 0.67 or market_rank_percentile < 0.33")

        ###  build 1/n long portfolio to compare with etf benchmark 

        return "111"
    
    def run(self):

        return "1111"

if __name__ == '__main__':
    run = portfolio_base()
    # run.load_base_factor_rank()
    run.load_liquid_bond_return(
        cusip_ids = ['001055AC6','001055AD4','001055AE2'],
        month_year = '2014-12'
    )
    run.build_portfolio()
