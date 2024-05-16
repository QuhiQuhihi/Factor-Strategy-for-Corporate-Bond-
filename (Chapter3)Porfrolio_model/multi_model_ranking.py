import os
import sys
import warnings
warnings.filterwarnings("ignore")

import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class rank_multi_factor:
    def __init__(self):
        self.start_date = '20140501'
        self.eval_date = '20240501'
        print("current dir is : ", os.getcwd())
        self.current_dir = os.getcwd()
        self.main_dir = os.path.join("C:\\", 'workspace', 'Factor-Strategy-for-Corporate-Bond-')
        print("main dir is : ", self.main_dir)
        self.data_dir = os.path.join(self.main_dir, "(Chapter1)Data")
        print("data dir is : ", self.data_dir)

    def load_calc_base_factor(self):
        # creating file path
        os.chdir(self.data_dir)
        dbfile = 'TRACE.db'
        # Create a SQL connection to our SQLite database
        conn = sqlite3.connect(dbfile)
        print("{} is connected for {}".format(dbfile, "load_multi_factor_data function"))
        # creating cursor
        cursor = conn.cursor()

        # Calculating and Loading market factor
        query = """
        with cbm_ranked_factor as (
            select month_year, cusip_id, 
                RANK() over (
                PARTITION by month_year
                order by CreditSpread DESC 
                ) csp_rank,
                Rank() over (
                partition by month_year
                order by "Duration*" desc
                ) dur_rank,
                Rank() over (
                partition by month_year
                order by Yieldtomaturity desc
                ) ytm_rank,  
                Rank() over (
                partition by month_year
                order by Volatility asc
                ) vol_rank,  
                Rank() over (
                partition by month_year
                order by "Skewness*" desc
                ) skew_rank,   
                Rank() over (
                partition by month_year
                order by "3m.Momentum" desc
                ) _3m_mom_rank, 
                Rank() over (
                partition by month_year
                order by "6m.Momentum" desc
                ) _6m_mom_rank, 
                Rank() over (
                partition by month_year
                order by "Book-to-price" asc
                ) pbr_rank,  
                Rank() over (
                partition by month_year
                order by "Default-beta" asc
                ) default_beta_rank, 
                Rank() over (
                partition by month_year
                order by "VaR(10%)"  asc
                ) var_rank,  
                Rank() over (
                partition by month_year
                order by "EquityMomentum" desc
                ) equity_mom_rank,
                RANK() over (
                PARTITION by month_year
                order by market DESC 
                ) market_rank,
                RANK() over (
                PARTITION by month_year
                order by term DESC 
                ) term_rank
            from coef_multi_model
            ), 
            cbm_datapoint as (
            select month_year, count(*) as total_num
            from coef_multi_model
            group by month_year 
            order by month_year
        )
        select cbm_ranked_factor.month_year, cbm_datapoint.total_num,
            cbm_ranked_factor.dur_rank, 
            cbm_ranked_factor.csp_rank, 
            cbm_ranked_factor.ytm_rank, 
            cbm_ranked_factor.vol_rank, 
            cbm_ranked_factor.skew_rank, 
            cbm_ranked_factor._3m_mom_rank, 
            cbm_ranked_factor._6m_mom_rank, 
            cbm_ranked_factor.pbr_rank, 
            cbm_ranked_factor.default_beta_rank, 
            cbm_ranked_factor.var_rank, 
            cbm_ranked_factor.equity_mom_rank, 
            cbm_ranked_factor.market_rank, 
            cbm_ranked_factor.term_rank, 
            cast(cbm_ranked_factor.dur_rank as float)/cbm_datapoint.total_num as dur_rank_percentile,
            cast(cbm_ranked_factor.csp_rank as float)/cbm_datapoint.total_num as csp_rank_percentile,
            cast(cbm_ranked_factor.ytm_rank as float)/cbm_datapoint.total_num as ytm_rank_percentile,
            cast(cbm_ranked_factor.vol_rank as float)/cbm_datapoint.total_num as vol_rank_percentile,
            cast(cbm_ranked_factor.skew_rank as float)/cbm_datapoint.total_num as skew_rank_percentile,
            cast(cbm_ranked_factor._3m_mom_rank as float)/cbm_datapoint.total_num as _3m_mom_rank_percentile,
            cast(cbm_ranked_factor._6m_mom_rank as float)/cbm_datapoint.total_num as _6m_mom_rank_percentile,
            cast(cbm_ranked_factor.pbr_rank as float)/cbm_datapoint.total_num as pbr_rank_percentile,
            cast(cbm_ranked_factor.default_beta_rank as float)/cbm_datapoint.total_num as default_beta_rank_percentile,
            cast(cbm_ranked_factor.var_rank as float)/cbm_datapoint.total_num as var_rank_percentile,
            cast(cbm_ranked_factor.equity_mom_rank as float)/cbm_datapoint.total_num as equity_mom_rank_percentile,
            cast(cbm_ranked_factor.market_rank as float)/cbm_datapoint.total_num as market_rank_percentile,
            cast(cbm_ranked_factor.term_rank as float)/cbm_datapoint.total_num as term_rank_percentile,
        from cbm_ranked_factor
        inner join cbm_datapoint
        on cbm_ranked_factor.month_year = cbm_datapoint.month_year
        order by cbm_ranked_factor.month_year asc
                ; """
        
        df=(cursor.execute(query)).fetchall()
        print("market factor is loaded")
        column_headers = [description[0] for description in cursor.description]
        factor_rank_data=pd.DataFrame(df,columns=column_headers)
        
        conn.commit()
        conn.close()
        os.chdir(self.current_dir)
        
        print(factor_rank_data)
        factor_rank_data.to_csv("multi_factor_rank.csv")
        return factor_rank_data
    
    def run(self):
        base_rank = self.load_calc_base_factor()
        return base_rank

if __name__ == '__main__':
    run = rank_multi_factor()
    run.run()
   