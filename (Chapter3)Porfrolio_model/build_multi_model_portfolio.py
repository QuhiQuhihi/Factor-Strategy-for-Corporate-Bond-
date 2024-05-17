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
        self.df_multi_rank['term_signal'] = 0
        self.df_multi_rank['market_signal'] = 0

        self.month_year_multi_rank = self.df_multi_rank['month_year'].unique()
        print(self.month_year_multi_rank)

        print("current dir is : ", os.getcwd())
        self.main_dir = os.path.join("C:\\", 'workspace', 'Factor-Strategy-for-Corporate-Bond-')
        print("main dir is : ", self.main_dir)
        self.data_dir = os.path.join(self.main_dir, "(Chapter1)Data")
        print("data dir is : ", self.data_dir)

    def assign_signals(self):
        # Example for market and term signals, expand similarly for other factors
        factors = [
            'market_signal', 'term_signal', 'dur_signal', 'csp_signal', 
            'ytm_signal', 'vol_signal', 'skew_signal', '_3m_mom_signal',
            '_6m_mom_signal', 'pbr_signal', 'default_beta_signal', 'var_signal',
            'equity_mom_signal'
        ]
        
        for factor in factors:
            self.df_multi_rank.loc[self.df_multi_rank[factor] < 0.33, factor] = 1
            self.df_multi_rank.loc[self.df_multi_rank[factor] > 0.66, factor] = -1
            self.df_multi_rank[factor] = self.df_multi_rank[factor].apply(lambda x: 0 if x not in [-1, 1] else x)


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

    def build_portfolio_old(self):
        
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

        # long market signal if rank is top 33%
        self.df_multi_rank['market_signal'].apply((lambda x: 1 if x < 0.33 else x))
        # short market signal if rank is bottom 33%
        self.df_multi_rank['market_signal'].apply((lambda x: -1 if x > 0.66 else x))

        # long term signal if rank is top 33%
        self.df_multi_rank['term_signal'].apply((lambda x: 1 if x < 0.33 else x))
        # short term signal if rank is bottom 33%
        self.df_multi_rank['term_signal'].apply((lambda x: -1 if x > 0.66 else x))

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
    

    def calculate_portfolio_returns(self):
        # First, let's ensure the data is merged appropriately
        # self.df_base_portfolio_weight = self.build_portfolio()  # Assuming build_portfolio returns the portfolio weights DataFrame
        factors = [
            'market_signal', 'term_signal', 'dur_signal', 'csp_signal', 
            'ytm_signal', 'vol_signal', 'skew_signal', '_3m_mom_signal',
            '_6m_mom_signal', 'pbr_signal', 'default_beta_signal', 'var_signal',
            'equity_mom_signal'
        ]
        # Initialize a DataFrame to store portfolio returns
        portfolio_monthly_returns = pd.DataFrame(columns=['month_year', 'market_signal_return', 'term_signal_return', 'dur_signal_return', 'csp_signal_return', 
            'ytm_signal_return', 'vol_signal_return', 'skew_signal_return', '_3m_mom_signal_return',
            '_6m_mom_signal_return', 'pbr_signal_return', 'default_beta_signal_return', 'var_signal_return',
            'equity_mom_signal_return'])

        for yyyy_mm in self.month_year_base_rank:
            # Get the signals and weights for the current month
            for factor in factors:
                current_month_signals = self.df_base_portfolio_weight[self.df_base_portfolio_weight['month_year'] == yyyy_mm]

                # Load bond returns for the next month
                next_month = pd.to_datetime(yyyy_mm) + pd.DateOffset(months=1)
                next_month = next_month.strftime('%Y-%m')  # Convert to string format YYYY-MM
                if next_month in self.month_year_base_rank:  # Ensure we have return data for the next month
                    next_month_returns = self.load_liquid_bond_return(cusip_ids = ['001055AC6','001055AD4','001055AE2'], month_year = '2014-12')
                    
                    # Merge signals with next month's returns
                    merged_data = pd.merge(current_month_signals, next_month_returns, on='cusip_id', how='left', suffixes=('', '_next'))

                    # Calculate the weighted returns
                    merged_data['weighted_returns_market'] = merged_data['market_weight'] * merged_data['log_returns']
                    merged_data['weighted_returns_term'] = merged_data['term_weight'] * merged_data['log_returns']
                    monthly_return_market = merged_data['weighted_returns_market'].sum()
                    monthly_return_term = merged_data['weighted_returns_term'].sum()

                    # Store the results
                    new_row = pd.DataFrame({
                        'month_year': [next_month],
                        'portfolio_return_market': [monthly_return_market],
                        'portfolio_return_term': [monthly_return_term]
                    })
                    portfolio_monthly_returns = pd.concat([portfolio_monthly_returns, new_row], ignore_index=True)


        return portfolio_monthly_returns

    
    def build_portfolio(self):
        self.df_base_portfolio_weight = pd.DataFrame()
        factors = [
            'market_signal', 'term_signal', 'dur_signal', 'csp_signal', 
            'ytm_signal', 'vol_signal', 'skew_signal', '_3m_mom_signal',
            '_6m_mom_signal', 'pbr_signal', 'default_beta_signal', 'var_signal',
            'equity_mom_signal'
        ]
        for factor in factors:
            self.df_multi_rank.loc[self.df_multi_rank[factor] < 0.33, factor] = 1
            self.df_multi_rank.loc[self.df_multi_rank[factor] > 0.66, factor] = -1
            self.df_multi_rank[factor] = self.df_multi_rank[factor].apply(lambda x: 0 if x not in [-1, 1] else x)

        for yyyy_mm in self.month_year_base_rank:
            monthly_rank = self.df_base_rank[self.df_base_rank['month_year'] == yyyy_mm]
            for factor in factors:
                long_weights = monthly_rank[monthly_rank[factor] == 1][factor].count()
                short_weights = monthly_rank[monthly_rank[factor] == -1][factor].count()
                neutral_weights= monthly_rank[monthly_rank[factor] == 0][factor].count()

                monthly_rank.loc[monthly_rank[factor] == 1, '{}_weight'.format(factor)] = 1 / long_weights if long_weights > 0 else 0
                monthly_rank.loc[monthly_rank[factor] == -1, '{}_weight'.format(factor)] = -1 / short_weights if short_weights > 0 else 0
                monthly_rank.loc[monthly_rank[factor] == 0, '{}_weight'.format(factor)] = 0  # Optionally, assign zero weight to neutral signals

                self.df_base_portfolio_weight = pd.concat([self.df_base_portfolio_weight, monthly_rank], ignore_index=True)



        

        for yyyy_mm in self.month_year_base_rank:
            monthly_rank = self.df_base_rank[self.df_base_rank['month_year'] == yyyy_mm]
            # Calculate weights for long and short positions
            long_weights_market = monthly_rank[monthly_rank['market_signal'] == 1]['market_signal'].count()
            short_weights_market = monthly_rank[monthly_rank['market_signal'] == -1]['market_signal'].count()
            neutral_weights_market= monthly_rank[monthly_rank['market_signal'] == 0]['market_signal'].count()

            # Calculate weights for long and short positions
            long_weights_term = monthly_rank[monthly_rank['term_signal'] == 1]['term_signal'].count()
            short_weights_term = monthly_rank[monthly_rank['term_signal'] == -1]['term_signal'].count()
            neutral_weights_term= monthly_rank[monthly_rank['term_signal'] == 0]['term_signal'].count()

            # Assign equal weights to each section of the portfolio
            monthly_rank.loc[monthly_rank['market_signal'] == 1, 'market_weight'] = 1 / long_weights_market if long_weights_market > 0 else 0
            monthly_rank.loc[monthly_rank['market_signal'] == -1, 'market_weight'] = -1 / short_weights_market if short_weights_market > 0 else 0
            monthly_rank.loc[monthly_rank['market_signal'] == 0, 'market_weight'] = 0  # Optionally, assign zero weight to neutral signals

            # Assign equal weights to each section of the portfolio
            monthly_rank.loc[monthly_rank['term_signal'] == 1, 'term_weight'] = 1 / long_weights_term if long_weights_term > 0 else 0
            monthly_rank.loc[monthly_rank['term_signal'] == -1, 'term_weight'] = -1 / short_weights_term if short_weights_term > 0 else 0
            monthly_rank.loc[monthly_rank['term_signal'] == 0, 'term_weight'] = 0  # Optionally, assign zero weight to neutral signals


            self.df_base_portfolio_weight = pd.concat([self.df_base_portfolio_weight, monthly_rank], ignore_index=True)
        portfolio_monthly_returns=self.calculate_portfolio_returns()
        # self.calculate_portfolio_returns()
        return portfolio_monthly_returns


    def run(self):

        return "1111"

if __name__ == '__main__':
    run = portfolio_multi()
    # run.load_base_factor_rank()
    run.load_liquid_bond_return(
        cusip_ids = ['001055AC6','001055AD4','001055AE2'],
        month_year = '2014-12'
    )
    run.build_portfolio()
