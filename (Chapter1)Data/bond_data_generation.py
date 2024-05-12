import os
import sys
import warnings
warnings.filterwarnings("ignore")

import sqlite3
import numpy as np
import pandas as pd

class data_bond:
    def __init__(self):
        self.start_date = '20140501'
        self.eval_date = '20240501'
        # print("main dir is : ", os.getcwd())
        # os.chdir(os.path.join(os.getcwd(), 'data'))
        # print("data dir is : ", os.getcwd())

        self.run()

    def filter_fisd(self,fisd):
        #* ************************************** */
        #* Filter fisd file                       */
        #* ************************************** */ 
        fisd = fisd[(fisd.interest_frequency != "-1") ]   # Unclassified by Mergent
        fisd = fisd[(fisd.interest_frequency != "13") ]   # Variable Coupon (V)
        fisd = fisd[(fisd.interest_frequency != "14") ]   # Bi-Monthly Coupon
        fisd = fisd[(fisd.interest_frequency != "16") ]   # Unclassified by Mergent
        fisd = fisd[(fisd.interest_frequency != "15") ]   # Unclassified by Mergent
        fisd = fisd[(~fisd.interest_frequency.isnull()) ] # Unclassified by Mergent
        fisd = fisd[(~fisd.offering_date.isnull()) ] # Unclassified by Mergent
        fisd['day_count_basis'] = np.where(fisd['day_count_basis'].isnull(),
                                        "30/360", fisd['day_count_basis'])
    
    def data_parse(self, traced):
        # Step 1: I do not have enough manpower to manually
        # inspect all of these non-1000 par bonds
        # ----> Only keep bonds with par of 1000, 10, 5000, 2000
        # i.e. those which are most frequent #
        par_mask = ((traced.principal_amt == 1000) |\
                    (traced.principal_amt == 10)   |\
                    (traced.principal_amt == 5000) |\
                    (traced.principal_amt == 2000)  )
        traced = traced[par_mask]

        # Step 2: $10 Par Bonds Inspection
        tracednon10 = traced[traced['principal_amt'] == 10]

        # Examine pricing
        tracednon10.groupby("interest_frequency")['pr'].mean()
        tracednon10.groupby("interest_frequency")['coupon'].mean()
        tracednon10.groupby("interest_frequency")['pr'].count()

        # Examine all bonds without semi-annual coupons
        tracednon10_semi = tracednon10[tracednon10["interest_frequency"] != '2']
        tracednon10_semi.groupby("interest_frequency")['pr'].mean()
        tracednon10_semi.groupby("interest_frequency")['pr'].count()

        # All bond except those with frequency == 2 have prices which correctly match
        # there par values (10)
        # Step 2.1: Scale all bonds (par==10) whose int_freq != 2 to be in 100 range 
        # Note: Coupons (if any) can remain as is / they seem correct
        mask_scale = ( (traced.principal_amt      == 10)&\
                    (traced.interest_frequency != '2') )
        traced.loc[mask_scale, 'prc_ew'] = traced.loc[mask_scale, 'prc_ew'] * 10
        traced.loc[mask_scale, 'pr']     = traced.loc[mask_scale, 'pr']     * 10

        # Outcome, all of the par == 10 bonds have correctly scaled prices #

        # Step 3: Par values of $5000
        tracednon5 = traced[traced['principal_amt'] == 5000]

        # Examine pricing
        tracednon5.groupby("interest_frequency")['pr'].mean()
        tracednon5.groupby("interest_frequency")['coupon'].mean()
        tracednon5.groupby("interest_frequency")['pr'].count()

        # Can leave the prices unchanged

        # Step 4: Par values of $2000
        tracednon2 = traced[traced['principal_amt'] == 2000]

        # Examine pricing
        tracednon2.groupby("interest_frequency")['pr'].mean()
        tracednon2.groupby("interest_frequency")['pr'].count()

        # Can leave the prices unchanged

        # Check #
        traced['principal_amt'].value_counts(normalize = True)*100
        traced.groupby("interest_frequency")['pr'].mean()
        traced.groupby(["principal_amt","interest_frequency"])['pr'].mean()

    def clean_bond_data(self,fisd):
        #* ************************************** */
        #* Apply BBW Bond Filters                 */
        #* ************************************** */  
        #1: Discard all non-US Bonds (i) in BBW
        fisd = fisd[(fisd.country_domicile == 'USA')]

        #2.1: US FX
        fisd = fisd[(fisd.foreign_currency == 'N')]

        #3: Must have a fixed coupon
        fisd = fisd[(fisd.coupon_type != 'V')]

        #4: Discard ALL convertible bonds
        fisd = fisd[(fisd.convertible == 'N')]

        #5: Discard all asset-backed bonds
        fisd = fisd[(fisd.asset_backed == 'N')]

        #6: Discard all bonds under Rule 144A
        fisd = fisd[(fisd.rule_144a == 'N')]

        #7: Remove Agency bonds, Muni Bonds, Government Bonds, 
        mask_corp = ((fisd.bond_type != 'TXMU')&  (fisd.bond_type != 'CCOV') &  (fisd.bond_type != 'CPAS')\
                    &  (fisd.bond_type != 'MBS') &  (fisd.bond_type != 'FGOV')\
                    &  (fisd.bond_type != 'USTC')   &  (fisd.bond_type != 'USBD')\
                    &  (fisd.bond_type != 'USNT')  &  (fisd.bond_type != 'USSP')\
                    &  (fisd.bond_type != 'USSI') &  (fisd.bond_type != 'FGS')\
                    &  (fisd.bond_type != 'USBL') &  (fisd.bond_type != 'ABS')\
                    &  (fisd.bond_type != 'O30Y')\
                    &  (fisd.bond_type != 'O10Y') &  (fisd.bond_type != 'O3Y')\
                    &  (fisd.bond_type != 'O5Y') &  (fisd.bond_type != 'O4W')\
                    &  (fisd.bond_type != 'CCUR') &  (fisd.bond_type != 'O13W')\
                    &  (fisd.bond_type != 'O52W')\
                    &  (fisd.bond_type != 'O26W')\
                    # Remove all Agency backed / Agency bonds #
                    &  (fisd.bond_type != 'ADEB')\
                    &  (fisd.bond_type != 'AMTN')\
                    &  (fisd.bond_type != 'ASPZ')\
                    &  (fisd.bond_type != 'EMTN')\
                    &  (fisd.bond_type != 'ADNT')\
                    &  (fisd.bond_type != 'ARNT'))
        fisd = fisd[(mask_corp)]

        #8: No Private Placement
        fisd = fisd[(fisd.private_placement == 'N')]

        #9: Remove floating-rate, bi-monthly and unclassified coupons
        fisd = fisd[(fisd.interest_frequency != 13) ] # Variable Coupon (V)

        #10 Remove bonds lacking information for accrued interest (and hence returns)
        fisd['offering_date']            = pd.to_datetime(fisd['offering_date'], 
                                                        format='%Y-%m-%d')
        fisd['dated_date']               = pd.to_datetime(fisd['dated_date'], 
                                                        format='%Y-%m-%d')
        fisd['maturity']               = pd.to_datetime(fisd['maturity'], 
                                                        format='%Y-%m-%d')

    def get_bond_data(self):
        # creating file path
        dbfile = 'TRACE.db'
        # Create a SQL connection to our SQLite database
        conn = sqlite3.connect(dbfile)
        print("{} is connected".format(dbfile))
        # creating cursor
        cursor = conn.cursor()

        # reading all table names
        table_list = [a for a in cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table'")]

        # Fetching data from master_corp_agency
        # query = """select * from master_corp_agency table
        #     master_corp_agency 
        #     where cusip_id in 
        #     (select distinct(cusip_id) as uniq_cusip from daily_btds)
        #     ;"""
        query = """select * from master_corp_agency  
            where cusip_id in 
            (select distinct(cusip_id) as uniq_cusip from daily_btds)
            ;"""
        df=(cursor.execute(query)).fetchall()
        print("TRACE.db information loaded")
        column_headers = [description[0] for description in cursor.description]
        master=pd.DataFrame(df,columns=column_headers)

        # Fetching data from daily_btds table
        query = "SELECT * FROM daily_btds"
        df=(cursor.execute(query)).fetchall()
        print("Fetched data from daily_btds table")
        column_headers = [description[0] for description in cursor.description]
        df_btds=pd.DataFrame(df,columns=column_headers)

        print("calculating investment grade bond return")
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
        print("Reindex the dataframe for each cusip_i")
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
        print("converting into monthly retun")
        # Calculate monthly log returns
        bond_prices['month_year'] = bond_prices['trans_dt'].dt.to_period('M')
        monthly_log_returns = bond_prices.groupby(['cusip_id', 'month_year'])['log_returns'].sum().reset_index()
        
        # handle extreme values. It cannot happen in fixed income market.
        monthly_log_returns['log_returns'] = df['log_returns'].apply(lambda x: 0.67 if x > 0.67 else x)
        monthly_log_returns['log_returns'] = df['log_returns'].apply(lambda x: -0.67 if x < -0.67 else x)

        print("completed")

        return monthly_log_returns
    
    def run(self):
        bond_data_result = self.get_bond_data()
        bond_data_result.to_csv("bond_data_result.csv")

if __name__ == '__main__':
    run = data_bond()
