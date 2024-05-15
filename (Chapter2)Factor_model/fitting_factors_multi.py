import os
import sys
import warnings
warnings.filterwarnings("ignore")

import sqlite3
import numpy as np
import pandas as pd

import statsmodels.api as sm

class factor_model:
    def __init__(self):
        self.start_date = '20140501'
        self.eval_date = '20240501'
        print("current dir is : ", os.getcwd())
        self.main_dir = os.path.join("C:\\", 'workspace', 'Factor-Strategy-for-Corporate-Bond-')
        print("main dir is : ", self.main_dir)
        self.data_dir = os.path.join(self.main_dir, "(Chapter1)Data")
        print("data dir is : ", self.data_dir)

        self.run()

    def load_multi_factor_data(self, table_names):
        # creating file path
        os.chdir(self.data_dir)
        dbfile = 'TRACE.db'
        # Create a SQL connection to our SQLite database
        conn = sqlite3.connect(dbfile)
        print("{} is connected for {}".format(dbfile, "load_base_factor_data function"))
        # creating cursor
        cursor = conn.cursor()


        for table_name in table_names:
            if table_name == 'factors_bond_mkt_term':
                query = """  
                    select * from factors_bond_mkt_term
                    WHERE date >= "2012-12-31" and date <= "2021-12-31"
                    ;"""
                df=(cursor.execute(query)).fetchall()
                print("market factor is loaded")
                column_headers = [description[0] for description in cursor.description]
                factors_bond_mkt_term=pd.DataFrame(df,columns=column_headers)
                factors_bond_mkt_term['date'] = pd.to_datetime(factors_bond_mkt_term['date'], format='%Y-%m-%d')
                factors_bond_mkt_term_col = column_headers
                factors_bond_mkt_term_col.pop(0)

            elif table_name == 'factors_bond_level':
                query = """  
                    select date, "Duration*" , CreditSpread , Yieldtomaturity , Volatility, "Skewness*", "3m.Momentum" ,"6m.Momentum" 
                    from factors_bond_level
                    WHERE date >= "2012-12-31" and date <= "2021-12-31" 
                    ;"""
                df=(cursor.execute(query)).fetchall()
                print("market factor is loaded")
                column_headers = [description[0] for description in cursor.description]
                factors_bond_level=pd.DataFrame(df,columns=column_headers)
                factors_bond_level['date'] = pd.to_datetime(factors_bond_level['date'], format='%Y-%m-%d')
                factors_bond_level_col = column_headers
                factors_bond_level_col.pop(0)

            elif table_name == 'factors_bond_firm_level':
                query = """  
                    select date, "Book-to-price", "Default-beta" , "VaR(10%)"  , EquityMomentum
                    from factors_bond_firm_level
                    WHERE date >= "2012-12-31" and date <= "2021-12-31"
                    ;"""
                df=(cursor.execute(query)).fetchall()
                print("market factor is loaded")
                column_headers = [description[0] for description in cursor.description]
                factors_bond_firm_level=pd.DataFrame(df,columns=column_headers)
                factors_bond_firm_level['date'] = pd.to_datetime(factors_bond_firm_level['date'], format='%Y-%m-%d')
                factors_bond_firm_level_col = column_headers
                factors_bond_firm_level_col.pop(0)
            else:
                print("please select vaild factor table name")

        # close session and change directory
        os.chdir(self.main_dir)
        conn.commit()
        conn.close()


        # Merge each tables
        # factor_data_result = factors_bond_mkt_term

        # # factor_data_result = factor_data_result.merge(factors_bond_mkt_term,left_index=True,right_index=True ,how='inner')
        # factor_data_result = factor_data_result.merge(factors_bond_level[factors_bond_level_col],left_index=True,right_index=True,how='inner', suffixes=('','') )
        # factor_data_result = factor_data_result.merge(factors_bond_firm_level[factors_bond_firm_level_col],left_index=True,right_index=True, how='inner', suffixes=('','') )


        factor_data_result = factors_bond_level
        factor_data_result = factor_data_result.merge(factors_bond_firm_level[factors_bond_firm_level_col],left_index=True,right_index=True, how='inner', suffixes=('bond','firm') )
        factor_data_result = factor_data_result.merge(factors_bond_mkt_term[factors_bond_mkt_term_col],left_index=True,right_index=True ,how='inner', suffixes=('',''))

        ### processing daily factor data to monthly
        
        # reindexing for monthly conversion
        print("Reindex the dataframe for each cusip_id")

        # Rename 'index' back to 'trans_dt'
        factor_data_result['date'] = pd.to_datetime(factor_data_result['date'], format='%Y-%m-%d')
        factor_data_result['month_year'] = factor_data_result['date'].dt.to_period('M')
        

        factor_data_result.drop(columns = ['date'], inplace=True)
        factor_data_result.set_index('month_year', inplace=True)

        for col in factor_data_result.columns.tolist():
            factor_data_result[col] = pd.to_numeric(factor_data_result[col], errors='coerce')

        # Calculate monthly log returns
        print("converting into monthly retun")
        monthly_avg_factor = factor_data_result.groupby(['month_year']).mean().reset_index()
        monthly_avg_factor.set_index('month_year', inplace=True)
        monthly_avg_factor.to_csv("factor_bond_multi_test.csv")

        return monthly_avg_factor

    
    def load_cusips(self):
        # creating file path
        os.chdir(self.data_dir)
        dbfile = 'TRACE.db'
        # Create a SQL connection to our SQLite database
        conn = sqlite3.connect(dbfile)
        print("{} is connected for {}".format(dbfile, "load_cusips function"))
        # creating cursor
        cursor = conn.cursor()

        query = """  
            select * from bond_liquid_cusip
            ;"""
        
        df=(cursor.execute(query)).fetchall()
        column_headers = [description[0] for description in cursor.description]
        liquid_cusip=pd.DataFrame(df,columns=column_headers)
        
        # close session and change directory
        os.chdir(self.main_dir)
        conn.commit()
        conn.close()

        return liquid_cusip

    def fitting_factor_by_cusip(self, cusip, factor_table):
        # creating file path
        os.chdir(self.data_dir)
        dbfile = 'TRACE.db'
        # Create a SQL connection to our SQLite database
        conn = sqlite3.connect(dbfile)
        print("{} is connected for {}".format(dbfile, "fitting_factor_by_cusip function {}".format(cusip)))
        # creating cursor
        cursor = conn.cursor()

        query = """  
            select * from bond_returns where cusip_id = "{}"
            ;""".format(cusip)
        
        df=(cursor.execute(query)).fetchall()
        column_headers = [description[0] for description in cursor.description]
        bond_price_match=pd.DataFrame(df,columns=column_headers)


        # close session and change directory
        os.chdir(self.main_dir)
        conn.commit()
        conn.close()

        bond_price_match = bond_price_match[['month_year', 'log_returns']]
        bond_price_date_list = bond_price_match['month_year'].unique().tolist()
                
        bond_price_match.set_index('month_year', inplace=True)

        # factor_table.set_index('month_year', inplace=True)
        factor_table_match = factor_table.loc[bond_price_date_list]
        
        # convert factor table's index datatype into str type to merge
        factor_table_match.index = factor_table_match.index.to_timestamp().strftime('%Y-%m')
        factor_table_match.index.name = None
        bond_price_match.index.name = None

        # Align X and y by index
        X_aligned, y_aligned = factor_table_match.align(bond_price_match, join='inner', axis=0)

        # dataframe to return monthly factor coefficient
        result_df = pd.DataFrame(
            columns=['cusip_id','month_year', 'const'] + factor_table_match.columns.tolist(),
        )


        # use past 8 month data to run stable OLS fitting
        for i in range(8,len(bond_price_date_list)):
            bond_date = bond_price_date_list[i]

            if i < 7:
                print("small data")
                bond_date_fit = bond_price_date_list[0:i+1]
            else:
                bond_date_fit = bond_price_date_list[i-8:i+1]
            
            X = X_aligned.loc[bond_date_fit]
            y = y_aligned.loc[bond_date_fit]

            result_parameters = [cusip, bond_date]

            X = sm.add_constant(X)
            ff_model = sm.OLS(y, X)
            results = ff_model.fit()

            # Combine the datasets
            # print(results.summary())

            for j in range(len(results.params)):
                result_parameters.append(results.params[j])

            result_df.loc[i-8] = result_parameters
        
        return result_df


    def generate_factor_fitting_table(self, df_new_fitting_result):
        index_new_start = len(self.result)
        len_new_df = len(df_new_fitting_result)

        if len(self.result) < 1:
            self.factor_list =  df_new_fitting_result.columns.tolist()
            self.result = pd.DataFrame(columns=self.factor_list)
        for i in range(len_new_df):
            self.result.loc[i + index_new_start] = df_new_fitting_result.iloc[i].tolist()

        print(df_new_fitting_result)




    

    def run(self):
        self.factor_table = self.load_multi_factor_data(["factors_bond_mkt_term","factors_bond_level", "factors_bond_firm_level"])
        self.factor_list = self.factor_table.columns.tolist()[3:]

        self.cusips_table = self.load_cusips()
        self.cusips_list_unique = self.cusips_table['cusip_id'].unique().tolist()
        
        # this is not used... it was to match base factor model
        self.result = pd.DataFrame(
            columns=['cusip_id','month_year', 'const']
        )

        # for test purpose
        # for cusip in ["001055AC6"]:
        #     fitting_result = self.fitting_factor_by_cusip(cusip, self.factor_table)
        #     self.generate_factor_fitting_table(fitting_result)
        # self.result.to_csv("test_multi_Result.csv")


        i = 0
        for cusip in self.cusips_list_unique:
            fitting_result = self.fitting_factor_by_cusip(cusip, self.factor_table)
            self.generate_factor_fitting_table(fitting_result)
            print("{} of {} completed {} process completed".format(i, len(self.cusips_list_unique),round(i / len(self.cusips_list_unique), 4)))
            i = i + 1
        self.result.to_csv("test_multi_Result.csv")


        # for cusip in self.cusips_list_unique:
        #     self.fitting_factor_by_cusip(cusip)



if __name__ == '__main__':
    run = factor_model()