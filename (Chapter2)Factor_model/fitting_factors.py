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

    def load_base_factor_data(self, table_names):
        # creating file path
        os.chdir(self.data_dir)
        dbfile = 'TRACE.db'
        # Create a SQL connection to our SQLite database
        conn = sqlite3.connect(dbfile)
        print("{} is connected for {}".format(dbfile, "load_base_factor_data function"))
        # creating cursor
        cursor = conn.cursor()


        ######
        ######
        ##### have to merge tables horizontally
        for table_name in table_names:
            if table_name == 'factors_bond_mkt_term':
                query = """  
                    select * from factors_bond_mkt_term
                    WHERE date >= "2012-12-31" and date <= "2021-12-31"
                    ;"""
                df=(cursor.execute(query)).fetchall()
                print("market factor is loaded")
                column_headers = [description[0] for description in cursor.description]
                factor_data=pd.DataFrame(df,columns=column_headers)
                # print(factor_data)
            
            elif table_name == 'factorfactors_bond_level':
                query = """  
                    select * from factors_bond_level
                    WHERE date >= "2012-12-31" and date <= "2021-12-31" 
                    ;"""
                df=(cursor.execute(query)).fetchall()
                print("market factor is loaded")
                column_headers = [description[0] for description in cursor.description]
                factor_data=pd.DataFrame(df,columns=column_headers)
                # print(factor_data)
            
            elif table_name == 'factors_bond_firm_level':
                query = """  
                    select * from factors_bond_firm_level
                    WHERE date >= "2012-12-31" and date <= "2021-12-31"
                    ;"""
                df=(cursor.execute(query)).fetchall()
                print("market factor is loaded")
                column_headers = [description[0] for description in cursor.description]
                factor_data=pd.DataFrame(df,columns=column_headers)
                # print(factor_data)
            else:
                print("please select vaild factor table name")

        # close session and change directory
        os.chdir(self.main_dir)
        conn.commit()
        conn.close()

        ### processing daily factor data to monthly
        
        # reindexing for monthly conversion
        print("Reindex the dataframe for each cusip_id")

        # convert str type date column into 
        factor_data['date'] = pd.to_datetime(factor_data['date'], format='%Y-%m-%d')


        # Rename 'index' back to 'trans_dt'
        # factor_data.rename(columns={'index': 'trans_dt'}, inplace=True)
        factor_data['month_year'] = factor_data['date'].dt.to_period('M')

        # Calculate monthly log returns
        print("converting into monthly retun")
        monthly_avg_factor = factor_data.groupby(['month_year']).mean().reset_index()
        monthly_avg_factor.drop(columns = ['date'], inplace=True)
        # print(monthly_avg_factor)

        monthly_avg_factor.set_index('month_year', inplace=True)
        monthly_avg_factor.to_csv("factors_bond_mkt_term_test.csv")

        return monthly_avg_factor


    def load_multi_factor_data(self, table_names):
        # creating file path
        os.chdir(self.data_dir)
        dbfile = 'TRACE.db'
        # Create a SQL connection to our SQLite database
        conn = sqlite3.connect(dbfile)
        print("{} is connected for {}".format(dbfile, "load_base_factor_data function"))
        # creating cursor
        cursor = conn.cursor()

        factor_data_result = pd.DataFrame()
        ######
        ######
        ##### have to merge tables horizontally
        
        table_name = 'factors_bond_mkt_term'
        query = """  
            select * from factors_bond_mkt_term
            WHERE date >= "2012-12-31" and date <= "2021-12-31"
            ;"""
        df=(cursor.execute(query)).fetchall()
        print("market factor is loaded")
        column_headers = [description[0] for description in cursor.description]
        factor_data_base=pd.DataFrame(df,columns=column_headers)
        factor_data_base['date'] = pd.to_datetime(factor_data_base['date'], format='%Y-%m-%d')
        
        # print(factor_data)


        for table_name in table_names:
            if table_name == 'factors_bond_mkt_term':
                continue

            elif table_name == 'factors_bond_level':
                query = """  
                    select * from factors_bond_level
                    WHERE date >= "2012-12-31" and date <= "2021-12-31" 
                    ;"""
                df=(cursor.execute(query)).fetchall()
                print("market factor is loaded")
                column_headers = [description[0] for description in cursor.description]
                factor_data=pd.DataFrame(df,columns=column_headers)
                factor_data['date'] = pd.to_datetime(factor_data['date'], format='%Y-%m-%d')
                # print(factor_data)
            
            elif table_name == 'factors_bond_firm_level':
                query = """  
                    select * from factors_bond_firm_level
                    WHERE date >= "2012-12-31" and date <= "2021-12-31"
                    ;"""
                df=(cursor.execute(query)).fetchall()
                print("market factor is loaded")
                column_headers = [description[0] for description in cursor.description]
                factor_data=pd.DataFrame(df,columns=column_headers)
                factor_data['date'] = pd.to_datetime(factor_data['date'], format='%Y-%m-%d')
                # print(factor_data)
            else:
                print("please select vaild factor table name")


            factor_data_result = factor_data_base.merge(factor_data,left_index=True,right_index=True )


        # close session and change directory
        os.chdir(self.main_dir)
        conn.commit()
        conn.close()

        ### processing daily factor data to monthly
        
        # reindexing for monthly conversion
        print("Reindex the dataframe for each cusip_id")

        # convert str type date column into 
        # factor_data['date'] = pd.to_datetime(factor_data['date'], format='%Y-%m-%d')


        # Rename 'index' back to 'trans_dt'
        # factor_data.rename(columns={'index': 'trans_dt'}, inplace=True)
        factor_data_result.drop(columns = ['date_y'], inplace=True)
        factor_data_result['month_year'] = factor_data_result['date_x'].dt.to_period('M')
        factor_data_result.drop(columns = ['date_x'], inplace=True)

        factor_data_result.set_index('month_year', inplace=True)
        for col in factor_data_result.columns.tolist():
            factor_data_result[col] = pd.to_numeric(factor_data_result[col], errors='coerce')

        # Calculate monthly log returns
        print("converting into monthly retun")
        monthly_avg_factor = factor_data_result.groupby(factor_data_result.index).mean()
        # monthly_avg_factor = factor_data_result.groupby(['month_year']).mean().reset_index()
        monthly_avg_factor.reset_index(inplace=True)
        # monthly_avg_factor.set_index('month_year',inplace=True)

        # monthly_avg_factor.drop(columns = ['month_year'], inplace=True) ############


        monthly_avg_factor.to_csv("factors_multi_bond_mkt_term_test.csv")

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

        factor_table.set_index('month_year', inplace=True)
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
        
        print("fitting result")
        print(result_df)

        return result_df
    
    def fitting_factor_by_cusip_old(self, cusip, factors):
        """
        OLS fitting of bond return data and factor to derive coefficient

        Parameters:
            cusip (str): Path to the SQLite database file.
            factors (list): List of factor (column name in db)
            
        Returns:
            pd.DataFrame or None: coefficients of each factor by cusip and month_year
        """
        return "11111111111"



    def generate_factor_fitting_table(self, df_new_fitting_result):
        index_new_start = len(self.result)
        len_new_df = len(df_new_fitting_result)

        for i in range(len_new_df):
            self.result.loc[i + index_new_start] = df_new_fitting_result.iloc[i].tolist()

        print(self.result)

    def generate_multi_factor_fitting_table(self, df_new_fitting_result):
        index_new_start = len(self.multi_result)
        len_new_df = len(df_new_fitting_result)

        print("self.factor_multi_table in generate_multi_factor_fitting_table")
        print(df_new_fitting_result.columns)
        print(self.multi_result.columns)


        for i in range(len_new_df):
            self.multi_result.loc[i + index_new_start] = df_new_fitting_result.iloc[i].tolist()

        print(self.multi_result)


    

    def run(self):
        test_table = "factors_bond_mkt_term"
        self.factor_table = self.load_base_factor_data([test_table])
        self.factor_list = self.factor_table.columns.tolist()

        self.factor_multi_table = self.load_multi_factor_data(["factors_bond_level", "factors_bond_firm_level"])
        self.factor_multi_list = self.factor_multi_table.columns.tolist()

        self.cusips_table = self.load_cusips()
        self.cusips_list_unique = self.cusips_table['cusip_id'].unique().tolist()

        self.result = pd.DataFrame(
            columns=['cusip_id','month_year', 'const'] + self.factor_list
        )

        self.multi_result = pd.DataFrame(
            columns=['cusip_id','month_year', 'const'] + self.factor_multi_list

        )

        # for cusip in self.cusips_list_unique:
        #     fitting_result = self.fitting_factor_by_cusip(cusip, self.factor_table)
        #     self.generate_factor_fitting_table(fitting_result)

        # self.result.to_csv("test_Result.csv")



        # for cusip in self.cusips_list_unique:
        for cusip in ["001055AC6"]:
            fitting_result = self.fitting_factor_by_cusip(cusip, self.factor_multi_table)
            self.generate_multi_factor_fitting_table(fitting_result)
        self.result.to_csv("test_multi_Result.csv")


        # for cusip in self.cusips_list_unique:
        #     self.fitting_factor_by_cusip(cusip)



if __name__ == '__main__':
    run = factor_model()