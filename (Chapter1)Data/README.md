## Data
Corporate bond data are more complex for several reasons: (i) whereas each company has a single stock, a company can have more than 100 bonds outstanding, (ii) the set of outstanding bonds changes over time, and (iii) some bond series are highly illiquid and the raw data have numerous erroneous and real outliers.[(2)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4586652) Addressing these data challenges in our project was one of the most challenging tasks. Database file(TRACE.db) and script (.py and .sql) for data-cleaning does not reflect full journey to clean data. There were more hidden cleaning and explatorary data analysis works in this project. 

The period of data used in our project range from 2013 to 2023 (10 years). Unlike other empirical research which incorporate as much data period as possble, our project include recent 10 years data since it captures unique era called negative yield and correspoding dramatic movement of bond market. Below image from Schroder Asset Management report shows that our project period captures unique begin-end of zero interest rate and volatile credit market regime.
<div>
<img src="./image_chapter1/schroder_negative_yield.png" width="600" height="600">
<img src="./image_chapter1/schroder_credit_spread_breakdown.png" width="600" height="600">
</div>

For bond price data, our project used Trade Reporting and Compliance Engine (TRACE) database from WRDS. TRACE is a database managed by the Financial Industry Regulatory Authority (FINRA), a non-governmental organization that acts under the supervision of the Securities and Exchange Commission (SEC). TRACE was established to enhance market transparency by facilitating the mandatory reporting of over-the-counter (OTC) transactions in publicly traded U.S. corporate bonds, including debt securities issued by corporations and federal government agencies.


## TRACE Database by SEC
TRACE captures a comprehensive set of information regarding each bond transaction, including the bond's unique identifier (CUSIP), the transaction date and time, the price at which the bond was traded, and the transaction volume (i.e., the amount of the bond that was traded). This data provides a detailed and precise view of the secondary market activity for corporate bonds.

One of the unique aspects of TRACE is its ability to provide real-time, transaction-level price information. Prior to the implementation of TRACE, the bond market was considerably less transparent, with investors often struggling to find accurate pricing data. By making this information available, TRACE significantly enhances market transparency, allowing investors to make more informed decisions.

As mentioned, TRACE is managed by FINRA, which ensures compliance with its reporting requirements and oversees the dissemination of transaction data to promote fair and efficient markets. The primary users of TRACE data are institutional and retail investors, financial analysts, and researchers. These stakeholders use the data to assess current market conditions, perform historical analysis, and inform investment strategies. Our project used this database as researcher.

Despite its significant contributions to market transparency, TRACE has some limitations. First, while it covers a broad range of bond transactions, it does not include all types of fixed-income securities; for example, transactions involving municipal bonds and certain agency securities are not reported through TRACE. Additionally, there can be a delay in the reporting of block trades (large transactions), which might temporarily skew the perceived market activity or pricing. Lastly, the depth of data provided, while extensive, may still lack some granular details that could be pertinent for high-level analysis, such as the identity of the bond buyer or seller.


## Data Cleaning matters
Although TRACE database is one of the most powerful and shows high level of integrity for empirical research, this database does not integrity of analysis. This limitation is not specific limitation for our project only. Question about replicability of The Corporate Bond Factor Zoo project [(1)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4589786) has been arose by AQR's research team [(2)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4586652). However the author of The Corporate Bond Factor Zoo project initially claimed replication failure of cross-sectional corporate bond risk premium analysis as well [(8)](https://www.sciencedirect.com/science/article/pii/S0304405X18302095). Also, The Corporate Bond Factor Zoo project ICE datasets, while AQR project uses TRACE database. Based on this, our project claim that we cannot guarantee clear robust benchmark and replicability for this project. Rather we decided to derive implication from recent market data and build optimal strategy.
  
To enhance the reliability of our analysis on the corporate bond market, we apply stringent data cleaning rules to the transaction records obtained from the TRACE database. Specifically, we exclude bonds not publicly traded in the U.S. market, such as those issued via private placements, under Rule 144A, non-USD denominated bonds, and bonds issued by non-U.S. entities. We also remove structured notes, mortgage-backed or asset-backed securities, agency-backed securities, equity-linked, and convertible bonds. Additionally, we exclude bonds with floating coupon rates and those with less than one year until maturity. To ensure the robustness of our results, we replicate our analyses using the TRACE dataset curated by the Wharton Research Data Services (WRDS) data science team.

We observe that monthly prices in the TRACE database are recorded precisely at the end of each month, ensuring that monthly returns calculations consistently use month-end prices. This consistency is crucial when employing equity characteristics to compute bond factor returns. However, certain bonds may not have transactions recorded at these specific times, potentially leading to inaccuracies in empirical research. To address this, we employ interpolation techniques for missing data or for months with no trade activity, thus maintaining the continuity and accuracy of our return calculations.

In our study, we also encounter issues related to the discontinuity of operations by some companies, as evidenced by breaks in their unique identification codes. It is a well-established fact that stock tickers alone cannot reliably indicate continuity due to various corporate events such as mergers and acquisitions (M&A), or bankruptcy. To navigate these challenges, we utilize a Mapping Table from WRDS, which helps in tracking changes in company identifiers—CUSIPs, GVKEYs, and tickers—throughout different corporate events. The CUSIP is a nine-character alphanumeric code that uniquely identifies a North American financial security. The GVKEY is a unique identifier used by the Global Vantage database for individual companies, and a ticker is a stock's unique alphabetic name used on an exchange.

If tracking the historical lineage of a bond or issuer proves untenable, we opt to exclude such data from our research. This approach helps minimize the impact of data discontinuities on our analysis, ensuring the integrity and reliability of our empirical findings. This meticulous data management strategy underscores the importance of rigorous data verification in conducting robust financial research.


## Clean Price vs Drity Price
This was one of the most challenging task for our project. 


## Multi Factor Coefficient fitting

### Coefficient data from The Corporate bond Factor Zoo
this is based on ICE database. 
highly dependent on earnings factor.

factors besieds this have lower significance.

### Coefficient data from AQR

day by day data -- applicable to all bonds. We have to 
1. convert into monthly data.
2. multiply with Mike's factors
3. run regression
4. build portfolio (selection)

Bond Market and Term Structure Factors: CSV - Includes the bond market factor and a term structure factor.
bond_mkt_term.csv


Bond Factors: CSV - Contains factors specific to different bond categories.
bond_factors.csv

Firm-Level Bond Factors: CSV - Provides factors formed on synthetic firm-level bonds.
bond_firm_factors.csv


Equity Signal-Based Bond Factors: CSV - Features factors derived from equity signals.
equity_signals_all.csv


Clustered Equity Signal-Based Bond Factors: CSV - Includes factors based on clustered equity signals.
equity_signals_cluster.csv
