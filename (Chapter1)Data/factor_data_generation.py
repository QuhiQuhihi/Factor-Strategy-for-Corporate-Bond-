import os
import sys

import sqlite3
import numpy as np
import pandas as pd
from functools import partial

class data_factor:
    def __init__(self):
        self.start_date = '20'
        self.eval_date = '20240501'
        print("main dir is : ", os.getcwd())
        os.chdir(os.path.join(os.getcwd(), 'data'))
        print("data dir is : ", os.getcwd())

    def get_factor_data(self):
        # creating file path
        dbfile = 'TRACE.db'
        # Create a SQL connection to our SQLite database
        conn = sqlite3.connect(dbfile)

        # creating cursor
        cursor = conn.cursor()

        # reading all table names
        table_list = [a for a in cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table'")]

        print(table_list)
        return table_list
    



    

    def fetch_data_from_sqlite(db_file, query):
        """
        Fetches data from a SQLite database using the provided SQL query.

        Parameters:
            db_file (str): Path to the SQLite database file.
            query (str): SQL query to execute.
            
        Returns:
            pd.DataFrame or None: Fetched data as a DataFrame.
        """
        try:

            # Connect to the SQLite database file
            conn = sqlite3.connect(db_file)

            # creating cursor
            cursor = conn.cursor()

            # Execute the SQL query and fetch data into a DataFrame
            data=(cursor.execute(query)).fetchall()
            column_headers = [description[0] for description in cursor.description]
            results=pd.DataFrame(data,columns=column_headers)
            # Close the connection
            conn.close()

            return results

        except sqlite3.Error as e:
            print("Error fetching data from SQLite database:", e)
            return None
        
    def insert_data_into_table(self, db_file, table_name, data):
        """
        Insert data into the specified table in the central database.

        Parameters:
            db_file (str): Path to the SQLite database file.
            table_name (str): Name of the table to insert data into.
            data (DataFrame): DataFrame containing the data to insert.
        """
        try:
            conn = sqlite3.connect(db_file)
            data.to_sql(table_name, conn, if_exists='append', index=False)
            print("Data inserted into table '{}' successfully.".format(table_name))
            conn.close()

        except sqlite3.Error as e:
            print("Error inserting data into table:", e)



    class FactorInvesting:
        def __init__(self, data):
            self.data = data
            self.output = data[['public_date', 'cusip']]


        def applyCal(inputDataset, outputDataset, targetName):
            inputDataset['public_date'] = pd.to_datetime(inputDataset['public_date'])

            inputDataset['YearMonth'] = inputDataset['public_date'].dt.to_period('M')
            inputDataset.set_index('YearMonth', inplace=True)

            # Define a function to apply to each group to calculate 12-month change
            def calculate_12_month_sales_change(group, targetName: str):
                # Shift the sales data by 12 months
                group[f'{targetName}_%change'] = (group[targetName] - group[targetName].shift(12)) / group[targetName].shift(12)
                return group
            
            # Use functools.partial to pass additional arguments to the apply function
            partial_func = partial(calculate_12_month_sales_change, targetName=targetName)
            # Apply the function to each product group
            temp2Result = inputDataset[[targetName, 'cusip', 'public_date']].groupby('cusip').apply(partial_func)
            temp2Result.reset_index(drop = True,inplace= True)
    
            return pd.merge(outputDataset, temp2Result, on = ['cusip', 'public_date'])




        def calculate_credit_factors(self) -> pd.DataFrame: 

            # 1. Profitability Growth Rate
            #self.output['profit_growth_rate'] = self.input.groupby('cusip')['npm'].pct_change()
            #fin_ratio['profit_growth_rate'].fillna(0, inplace=True)

            db_file = 'TRACE.db'
            query = "SELECT * FROM wrds_fin_ratio LIMIT 10000"
            fin_ratio_data = fetch_data_from_sqlite(db_file, query)
                    #TODO replace with yearly mean instead of 0

            fin_ratio_data = fin_ratio_data.fillna(0)
            fin_ratio_data = fin_ratio_data.replace('',0)
            #fin_ratio_data = pd.read_csv('wrds_fin_ratio.csv')
            fin_ratio_data['public_date'] = pd.to_datetime(fin_ratio_data['public_date'])


            results = FactorInvesting.applyCal(fin_ratio_data, self.output, 'npm')
            results = FactorInvesting.applyCal(fin_ratio_data, results, 'debt_assets')
            results = FactorInvesting.applyCal(fin_ratio_data, results, 'opmbd')
            results = FactorInvesting.applyCal(fin_ratio_data, results, 'de_ratio')
            results = FactorInvesting.applyCal(fin_ratio_data, results, 'debt_capital')      
            results = FactorInvesting.applyCal(fin_ratio_data, results, 'debt_invcap')
            results = FactorInvesting.applyCal(fin_ratio_data, results, 'intcov_ratio')      
            results = FactorInvesting.applyCal(fin_ratio_data, results, 'quick_ratio')
            results = FactorInvesting.applyCal(fin_ratio_data, results, 'pcf')      
            results = FactorInvesting.applyCal(fin_ratio_data, results, 'ptb')

            return results
        
        # coefficient factor for bonds - to be used later 
        def calculate_bond_factors(self, changeYoY = False) -> pd.DataFrame: 

            # 1. Profitability Growth Rate
            #self.output['profit_growth_rate'] = self.input.groupby('cusip')['npm'].pct_change()
            #fin_ratio['profit_growth_rate'].fillna(0, inplace=True)

            db_file = 'TRACE.db'
            query = "SELECT * FROM bond_firm_factors"
            bond_firm_factors = fetch_data_from_sqlite(db_file, query)
            #bond_firm_factors = bond_firm_factors.fillna(0)
            #bond_firm_factors = pd.read_csv('bond_firm_factors.csv')

            bond_firm_factors['date'] = pd.to_datetime(bond_firm_factors['date'])    
            bond_firm_factors['YearMonth'] = bond_firm_factors['date'].dt.to_period('M')
            #compute the percentage change for selected bond firm factors.
            results_MoM = bond_firm_factors[['Duration*', '3m. Momentum', '6m. Momentum', 
                                        '9m. Momentum', '12m. Momentum', 'Yield to maturity', 
                                        'Credit Spread', 'Volatility']].pct_change()
            
            if changeYoY:
                #compute the percentage change YEAR OVER YEAR for selected bond firm factors.

                bond_firm_factors.set_index('YearMonth', inplace=True)
                selectedBond_factors = bond_firm_factors[['Duration*', '3m. Momentum', '6m. Momentum', 
                                                    '9m. Momentum', '12m. Momentum', 'Yield to maturity', 
                                                    'Credit Spread', 'Volatility']] 
                results_YoY = (selectedBond_factors - selectedBond_factors.shift(12)) / selectedBond_factors.shift(12)
                return results_YoY
            

            return results_MoM 
        
    #   def mergedFactor_df(df1 = calculate_credit_factors(), df2 = calculate_bond_factors()) ->pd.DataFrame:
    #      return pd.merge(df1, df2, on = ['YearMonth'])
        

        
        
        def create_factor_table(self, db_file):
            """
            Create a table named 'factor_finratio' in the central database to store the calculated factors.

            Parameters:
                db_file (str): Path to the SQLite database file.
            """
            try:
                conn = sqlite3.connect(db_file)
                cursor = conn.cursor()

                # Create 'factor_finratio' table
                cursor.execute('''CREATE TABLE IF NOT EXISTS Factor_FinRatio (
                                    factor_id INTEGER PRIMARY KEY,
                                    gvkey TEXT, permno TEXT, adate TEXT, 
                                    qdate TEXT, public_date TEXT, CAPEI REAL, 
                                    bm REAL, evm REAL, pe_op_basic REAL, 
                                    pe_op_dil REAL, pe_exi REAL, pe_inc REAL, 
                                    ps REAL, pcf REAL, dpr REAL, npm REAL, 
                                    opmbd REAL, opmad REAL, gpm REAL, ptpm REAL, 
                                    cfm REAL, roa REAL, roe REAL, roce REAL, 
                                    efftax REAL, aftret_eq REAL, aftret_invcapx REAL, 
                                    aftret_equity REAL, pretret_noa REAL, pretret_earnat REAL, 
                                    GProf REAL, equity_invcap REAL, debt_invcap REAL, totdebt_invcap REAL, 
                                    capital_ratio REAL, int_debt REAL, int_totdebt REAL, cash_lt REAL, 
                                    invt_act REAL, rect_act REAL, debt_at REAL, debt_ebitda REAL, 
                                    short_debt REAL, curr_debt REAL, lt_debt REAL, profit_lct REAL, 
                                    ocf_lct REAL, cash_debt REAL, fcf_ocf REAL, lt_ppent REAL, 
                                    dltt_be REAL, debt_assets REAL, debt_capital REAL, de_ratio REAL, 
                                    intcov REAL, intcov_ratio REAL, cash_ratio REAL, quick_ratio REAL, 
                                    curr_ratio REAL, cash_conversion REAL, inv_turn REAL, at_turn REAL, 
                                    rect_turn REAL, pay_turn REAL, sale_invcap REAL, sale_equity REAL, 
                                    sale_nwc REAL, rd_sale REAL, adv_sale REAL, staff_sale REAL, 
                                    accrual REAL, ptb REAL, PEG_trailing REAL, divyield REAL, 
                                    TICKER TEXT, cusip TEXT, profit_growth_rate REAL, noa_gr1a REAL, 
                                    saleq_gr1 REAL, curr_ratio_change REAL, quick_ratio_change REAL, 
                                    cash_ratio_change REAL, debt_me REAL, debt_assets_change REAL, 
                                    de_ratio_change REAL, debt_capital_change REAL, debt_invcap_change REAL, 
                                    earnings_growth_consistency REAL, roce_change REAL, aftret_invcapx_change REAL, 
                                    ptb_change REAL, peg_trailing_change REAL, efftax_change REAL, cowc_gr1a REAL, 
                                    nncoa_gr1a REAL, cop_at REAL, recurring_earnings_ratio REAL
                                )''')


                conn.commit()
                conn.close()

                print("Table 'Factor_FinRatio' created successfully.")

            except sqlite3.Error as e:
                print("Error creating table:", e)





    # Example Usage:
    if __name__ == "__main__":

        #data = pd.read_csv('wrds_fin_ratio.csv')
        db_file = 'TRACE.db'
        query = "SELECT * FROM wrds_fin_ratio LIMIT 10000"
        # TODO: error in running factor_investing.calculate_factors(data) when loading through database data = fetch_data_from_sqlite(db_file, query) but not through csv
        data = fetch_data_from_sqlite(db_file, query)
        #data = data.fillna(0)
        data['public_date'] = pd.to_datetime(data['public_date'])

        factor_investing = FactorInvesting(data)
        
        factor_results = factor_investing.calculate_credit_factors()
        #factor_bond_results = factor_investing.calculate_bond_factors(changeYoY = False)

        print("test factor results")
        print(factor_results.describe())
        factor_results['month_year'] = factor_results['public_date'].dt.to_period('M')

        factor_results.to_csv('factor_results.csv', index = False)

        
        #factor_investing.create_factor_table(db_file)  # Create factor table in the central database
        # Insert factor results into the central database
        #insert_data_into_table(db_file, 'Factor_FinRatio', factor_results)
        

    """
    return Factor_FinRatio database columns description:

    1. gvkey: Global company key
    2. permno: Permanent number assigned by CRSP
    3. adate: Announcement date
    4. qdate: Quarter end date
    5. public_date: Public date
    6. CAPEI: Cyclically adjusted price-to-earnings ratio
    7. bm: Book-to-market ratio
    8. evm: Enterprise value to sales ratio
    9. pe_op_basic: Operating income basic earnings per share
    10. pe_op_dil: Operating income diluted earnings per share
    11. pe_exi: Earnings per share excluding extraordinary items
    12. pe_inc: Earnings per share including extraordinary items
    13. ps: Price-to-sales ratio
    14. pcf: Price-to-cash flow ratio
    15. dpr: Dividend payout ratio
    16. npm: Net profit margin
    17. opmbd: Operating profit margin before depreciation
    18. opmad: Operating profit margin after depreciation
    19. gpm: Gross profit margin
    20. ptpm: Pretax profit margin
    21. cfm: Cash flow margin
    22. roa: Return on assets
    23. roe: Return on equity
    24. roce: Return on capital employed
    25. efftax: Effective tax rate
    26. aftret_eq: After-tax return on equity
    27. aftret_invcapx: After-tax return on invested capital
    28. aftret_equity: After-tax return on equity
    29. pretret_noa: Pretax return on net operating assets
    30. pretret_earnat: Pretax return on total assets
    31. GProf: Gross profit to sales ratio
    32. equity_invcap: Equity to invested capital ratio
    33. debt_invcap: Debt to invested capital ratio
    34. totdebt_invcap: Total debt to invested capital ratio
    35. capital_ratio: Capital ratio
    36. int_debt: Interest-bearing debt to total capital ratio
    37. int_totdebt: Interest-bearing total debt to total capital ratio
    38. cash_lt: Long-term cash ratio
    39. invt_act: Inventory turnover ratio
    40. rect_act: Receivables turnover ratio
    41. debt_at: Debt to total assets ratio
    42. debt_ebitda: Debt to EBITDA ratio
    43. short_debt: Short-term debt to total capital ratio
    44. curr_debt: Current debt to total capital ratio
    45. lt_debt: Long-term debt to total capital ratio
    46. profit_lct: Profit to liquidity ratio
    47. ocf_lct: Operating cash flow to liquidity ratio
    48. cash_debt: Cash to debt ratio
    49. fcf_ocf: Free cash flow to operating cash flow ratio
    50. lt_ppent: Long-term debt to property, plant, and equipment ratio
    51. dltt_be: Long-term debt to total equity ratio
    52. debt_assets: Debt to assets ratio
    53. debt_capital: Debt to capital ratio
    54. de_ratio: Debt equity ratio
    55. intcov: Interest coverage ratio
    56. intcov_ratio: Interest coverage ratio
    57. cash_ratio: Cash ratio
    58. quick_ratio: Quick ratio
    59. curr_ratio: Current ratio
    60. cash_conversion: Cash conversion cycle
    61. inv_turn: Inventory turnover ratio
    62. at_turn: Asset turnover ratio
    63. rect_turn: Receivables turnover ratio
    64. pay_turn: Payables turnover ratio
    65. sale_invcap: Sales to invested capital ratio
    66. sale_equity: Sales to equity ratio
    67. sale_nwc: Sales to net working capital ratio
    68. rd_sale: Research and development to sales ratio
    69. adv_sale: Advertising to sales ratio
    70. staff_sale: Staff to sales ratio
    71. accrual: Accruals
    72. ptb: Price-to-book ratio
    73. PEG_trailing: Trailing price/earnings to growth ratio
    74. divyield: Dividend yield
    75. TICKER: Stock ticker symbol
    76. profit_growth_rate: Profitability growth rate, calculated as the percentage change in net profit margin (`npm`) grouped by CUSIP number (`cusip`).
    77. cop_at: Ratio of operating profit margin before depreciation (`opmbd`) to the mean of equity to invested capital (`equity_invcap`) grouped by CUSIP number (`cusip`).
    78. noa_gr1a: Change in net operating assets (`roa`) grouped by CUSIP number (`cusip`).
    79. saleq_gr1: Percentage change in sales to invested capital (`sale_invcap`) grouped by CUSIP number (`cusip`).
    80. curr_ratio_change: Change in current ratio (`curr_ratio`) grouped by CUSIP number (`cusip`).
    81. quick_ratio_change: Change in quick ratio (`quick_ratio`) grouped by CUSIP number (`cusip`).
    82. cash_ratio_change: Change in cash ratio (`cash_ratio`) grouped by CUSIP number (`cusip`).
    83. debt_me: Debt management efficiency ratio, calculated as the ratio of total debt to invested capital (`totdebt_invcap`) to the mean of enterprise value to sales (`evm`) grouped by CUSIP number (`cusip`).
    84. debt_assets_change: Change in debt to assets ratio (`debt_assets`) grouped by CUSIP number (`cusip`).
    85. de_ratio_change: Change in debt equity ratio (`de_ratio`) grouped by CUSIP number (`cusip`).
    86. debt_capital_change: Change in debt to capital ratio (`debt_capital`) grouped by CUSIP number (`cusip`).
    87. debt_invcap_change: Change in debt to invested capital ratio (`debt_invcap`) grouped by CUSIP number (`cusip`).
    88. recurring_earnings_ratio: Ratio of operating profit margin after depreciation (`opmad`) to the mean of operating profit margin before depreciation (`opmbd`) grouped by CUSIP number (`cusip`).
    89. earnings_growth_consistency: Earnings growth consistency, calculated as the percentage change in operating income basic earnings per share (`pe_op_basic`) grouped by CUSIP number (`cusip`).
    90. roce_change: Change in return on capital employed (`roce`) grouped by CUSIP number (`cusip`).
    91. aftret_invcapx_change: Change in after-tax return on invested capital (`aftret_invcapx`) grouped by CUSIP number (`cusip`).
    92. ptb_change: Change in price-to-book ratio (`ptb`) grouped by CUSIP number (`cusip`).
    93. peg_trailing_change: Change in trailing price/earnings to growth ratio (`PEG_trailing`) grouped by CUSIP number (`cusip`).
    94. efftax_change: Change in effective tax rate (`efftax`) grouped by CUSIP number (`cusip`).
    95. cowc_gr1a: Change in current operating working capital (`ocf_lct`) grouped by CUSIP number (`cusip`).
    96. nncoa_gr1a: Change in net noncurrent operating assets (`aftret_invcapx`) grouped by CUSIP number (`cusip`).
    97. cop_at: Operating profit margin before depreciation (`opmbd`) to equity to invested capital (`equity_invcap`) ratio grouped by CUSIP number (`cusip`).
    98. recurring_earnings_ratio: Ratio of operating profit margin after depreciation (`opmad`) to the mean of operating profit margin before depreciation (`opmbd`) grouped by CUSIP number (`cusip`).

    These columns provide additional insights into various financial and operational aspects of the companies, calculated based on the original data columns.




    """


    def run(self):
        self.get_factor_data()

    

# if __init__=="__main__":
#     data_bond.get_bond_data()