import os
import sys
import warnings
warnings.filterwarnings("ignore")

import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# from base_model_ranking import rank_base_factor
from multi_model_ranking import rank_multi_factor

class portfolio_multi:
    def __init__(self):
        # Define the tickers and the date range
        self.start_date = '2013-12-31'
        self.end_date = '2023-12-31'

        # loading base_rank dataframe
        self.df_multi_rank = rank_multi_factor().run()

        self.df_multi_rank['dur_signal'] = 0
        self.df_multi_rank['csp_signal'] = 0
        self.df_multi_rank['ytm_signal'] = 0
        self.df_multi_rank['vol_signal'] = 0
        self.df_multi_rank['skew_signal'] = 0
        self.df_multi_rank['_3m_mom_signal'] = 0
        self.df_multi_rank['_6m_mom_signal'] = 0
        self.df_multi_rank['pbr_signal'] = 0
        self.df_multi_rank['default_beta_signal'] = 0
        self.df_multi_rank['var_signal'] = 0
        self.df_multi_rank['equity_mom_signal'] = 0

        self.month_year_multi_rank = self.df_multi_rank['month_year'].unique()
        print(self.month_year_multi_rank)

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
        print("{} is connected for {}".format(dbfile, "load_multi_factor_data function"))
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
        
        # long duration signal if rank is top 33%
        self.df_multi_rank['dur_signal'].apply((lambda x: 1 if x < 0.33 else x))
        # short duration signal if rank is bottom 33%
        self.df_multi_rank['dur_signal'].apply((lambda x: -1 if x > 0.66 else x))

        # credit spread signal if rank is top 33%
        self.df_multi_rank['csp_signal'].apply((lambda x: 1 if x < 0.33 else x))
        # credit spread signal if rank is bottom 33%
        self.df_multi_rank['csp_signal'].apply((lambda x: -1 if x > 0.66 else x))

        # yield to maturity signal if rank is top 33%
        self.df_multi_rank['ytm_signal'].apply((lambda x: 1 if x < 0.33 else x))
        # yield to maturity signal if rank is bottom 33%
        self.df_multi_rank['ytm_signal'].apply((lambda x: -1 if x > 0.66 else x))

        # bond volatility signal if rank is top 33%
        self.df_multi_rank['vol_signal'].apply((lambda x: 1 if x < 0.33 else x))
        # bond volatility signal if rank is bottom 33%
        self.df_multi_rank['vol_signal'].apply((lambda x: -1 if x > 0.66 else x))

        # bond return skewness signal if rank is top 33%
        self.df_multi_rank['skew_signal'].apply((lambda x: 1 if x < 0.33 else x))
        # bond return skewness signal if rank is bottom 33%
        self.df_multi_rank['skew_signal'].apply((lambda x: -1 if x > 0.66 else x))

        # 3 month bond momentum signal if rank is top 33%
        self.df_multi_rank['_3m_mom_signal'].apply((lambda x: 1 if x < 0.33 else x))
        # 3 month bond momentum signal if rank is bottom 33%
        self.df_multi_rank['_3m_mom_signal'].apply((lambda x: -1 if x > 0.66 else x))

        # 6 month bond momentum signal if rank is top 33%
        self.df_multi_rank['_6m_mom_signal'].apply((lambda x: 1 if x < 0.33 else x))
        # 6 month bond momentum signal if rank is bottom 33%
        self.df_multi_rank['_6m_mom_signal'].apply((lambda x: -1 if x > 0.66 else x))

        # book-to-price signal if rank is top 33%
        self.df_multi_rank['pbr_signal'].apply((lambda x: 1 if x < 0.33 else x))
        # book-to-price signal if rank is bottom 33%
        self.df_multi_rank['pbr_signal'].apply((lambda x: -1 if x > 0.66 else x))

        # default beta signal if rank is top 33%
        self.df_multi_rank['default_beta_signal'].apply((lambda x: 1 if x < 0.33 else x))
        # default beta signal if rank is bottom 33%
        self.df_multi_rank['default_beta_signal'].apply((lambda x: -1 if x > 0.66 else x))

        # VaR(10%) signal if rank is top 33%
        self.df_multi_rank['var_signal'].apply((lambda x: 1 if x < 0.33 else x))
        # VaR(10%) signal if rank is bottom 33%
        self.df_multi_rank['var_signal'].apply((lambda x: -1 if x > 0.66 else x))

        # equity momentum signal if rank is top 33%
        self.df_multi_rank['equity_mom_signal'].apply((lambda x: 1 if x < 0.33 else x))
        # equity momentum signal if rank is bottom 33%
        self.df_multi_rank['equity_mom_signal'].apply((lambda x: -1 if x > 0.66 else x))


        ###  build 1/n long and short portfolio to check whether this strategy works --> have to update for multi factor setting
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
