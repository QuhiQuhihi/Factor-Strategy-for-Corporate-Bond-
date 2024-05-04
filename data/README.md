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

[Paper] (https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4586652)
[Data Source] (https://www.stolborg.com/data)