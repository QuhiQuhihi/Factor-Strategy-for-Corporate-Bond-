import os
import sys
import warnings
warnings.filterwarnings("ignore")

import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class rank_base_factor:
    def __init__(self):
        self.start_date = '20140501'
        self.eval_date = '20240501'
        print("current dir is : ", os.getcwd())
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
        print("{} is connected for {}".format(dbfile, "load_base_factor_data function"))
        # creating cursor
        cursor = conn.cursor()

        # Calculating and Loading market factor
        query = """
                with cbm_ranked_factor as (
                    select month_year, cusip_id, 
                        RANK() over (
                        PARTITION by month_year
                        order by market DESC 
                        ) market_rank,
                        Rank() over (
                        partition by month_year
                        order by term desc
                        ) term_rank
                from coef_base_model), 
                    cbm_datapoint as (
                    select month_year, count(*) as total_num
                    from coef_base_model
                    group by month_year 
                    order by month_year
                )
                select cbm_ranked_factor.month_year, cbm_ranked_factor.market_rank, cbm_ranked_factor.term_rank, cbm_datapoint.total_num,
                    cast(cbm_ranked_factor.market_rank as float)/cbm_datapoint.total_num as market_rank_percentile,
                    cast(cbm_ranked_factor.term_rank as float)/cbm_datapoint.total_num as term_rank_percentile
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

        print(factor_rank_data)
        return factor_rank_data

    def run(self):
        self.load_calc_base_factor()

if __name__ == '__main__':
    run = rank_base_factor()
    run.run()
   