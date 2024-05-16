# Multi Factor Model for Corporate Bond
This research project is to build multi-factor model and optimization tools for corporate bond (credit market) market using empirical data. Traditional factor models including value-momentum showed explanability in asset pricing model across various asset classes. [(5)](https://www.aqr.com/Insights/Research/White-Papers/Long-Only-Style-Investing). Ever since CAPM and Famma French factor model are introduced, there were a lot of attempts to explain equity return and collective study proved that these risk factors are eithter useful, useless, or redundant to span cross-sectional equity return. [(6)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4605976)

Unlike equity market, there are not so many attempts to breakdown risk premium of credit bonds. Prominent research by Bai, Bali and Wen (2019) [(8)](https://www.sciencedirect.com/science/article/pii/S0304405X18302095) suggested common risk factors in cross-sectional return of corporate bond marekt. However, this research is retracted from Journal of Financial Econometrics in 2023 as subsequent research conducted by Dickerson, Mueller and Robotti (2023) [(9)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4398449) using a similar dataset of corporate bond returns reveals an error present in the data used by Bai et al. (2019) that consists of temporal misalignment of different data series.

 When expanding multi factor asset pricing model into fixed income market, the market shows its inherit incompleteness and proves multiple risk premium. For example, it is possible for one company to issue various bonds by setting differnt maturity, covenant, and collateral while there is one type of equity (besides prefered equity) This makes traders in credit market to consider multiple aspects with limited data. Also, structures embedded in fixed income securities, such as trench and secured, make valuation and execution difficult.  


## [Chapter 1 About Data](https://github.com/QuhiQuhihi/Factor-Strategy-for-Corporate-Bond-/blob/main/(Chapter1)Data/README.md)
This section is about the data sources and methodologies employed in our research project, emphasizing the integration of corporate bond trade data from the Trade Reporting and Compliance Engine (TRACE) database, managed by the Securities and Exchange Commission (SEC), and financial ratio data from Wharton Research Data Services (WRDS). The mandatory reporting requirement of corporate bond trades in TRACE offers rich insights into market dynamics, essential for constructing robust factor models.

Corporate bond data pose inherent complexities due to several factors: (i) a single company may have multiple bonds outstanding, often exceeding 100; (ii) the inventory of these bonds varies over time; and (iii) bond series can be illiquid with numerous anomalies in the data set, both erroneous and real. Addressing these challenges was a critical task in our project. We implemented rigorous filters to eliminate known data inaccuracies, followed by a meticulous manual review of extreme outliers. This method ensured the exclusion of errors while preserving data points that represent genuine economic events, thus maintaining high data integrity for subsequent modeling.

Moreover, the project leverages the WRDS database for corporate-level data, widely acknowledged and utilized within the academic community. This integration was crucial, albeit the project did not evaluate the database's internal consistency, instead directly incorporating its data into our model.

In summary, our project effectively constructed a comprehensive dataset for the asset pricing model, encapsulating significant nuances of the corporate bond market. Further details on the database structure and the data cleaning processes are elaborated upon in the subsequent sections of this paper.

## [Chapter 2 Simple Factor Model for credit](https://github.com/QuhiQuhihi/Factor-Strategy-for-Corporate-Bond-/blob/main/(Chapter2)Factor_model/README.md)
This section delves into the methodologies employed in the robust factor construction and regression analysis of corporate bond returns. Addressing replication failures in previous studies, a new framework utilizing clean data and rigorous statistical methods is proposed. The methodologies discussed include regression analysis of factor returns, long-short factor portfolio construction, robust factor construction techniques, and multiple testing corrections. The application of these methodologies aims to provide a more reliable framework for analyzing corporate bond returns, enhancing the reproducibility and validity of financial research in corporate bond markets.

## [Chapter 3 Portfolio for credit](https://github.com/QuhiQuhihi/Factor-Strategy-for-Corporate-Bond-/blob/main/(Chapter3)Porfrolio_model/README.md)
This chapter discusses the advantages of integrating various investment styles in long-only credit portfolios, compared to merely mixing them. This integration aims to enhance portfolio performance by capitalizing on the interactions between different styles. It contrasts the traditional mixed portfolio approach, where separate portfolios are simply combined, with an integrated approach that constructs portfolios through a unified strategy, resulting in higher returns and reduced costs. The empirical results favor the integrated approach, showing it offers better excess and risk-adjusted returns.

## [Chapter 4 Evaluating Performance](https://github.com/QuhiQuhihi/Factor-Strategy-for-Corporate-Bond-/blob/main/(Chapter4)Evaluation/README.md)

## [Chapter 5 Possible Application](https://github.com/QuhiQuhihi/Factor-Strategy-for-Corporate-Bond-/tree/main/(Chapter5)Application)
## Reference 

### (1) The Corporate Bond Factor Zoo
#### [Paper](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4589786) [data](https://openbondassetpricing.com/)
: This paper propose explanability of corporate bond return using various factors in bond, equity, macro, and fundamental data. 

### (2) AQR Corporate Bond Factors: Replication Failures and a New Framework
#### [paper](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4586652) [data](https://www.stolborg.com/data)  
: This paper deal with replication failure of Corporate Bond Factor Zoo by Dickerson, Alexander and Julliard, Christian and Mueller, Philippe, The Corporate Bond Factor Zoo (October 2, 2023). 

### (3) Vanguard’s portfolio construction framework
#### [paper](https://corporate.vanguard.com/content/dam/corp/research/pdf/vanguards_portfolio_construction_framework.pdf)
: This paper propose basic investing priciples and corresponding custom portfolio building. Our project review whether our proposed poftfolio strategy follows this protocol.

### (4) Long-Only Style Investing: Don't Just Mix, Integrate 
#### [paper](https://www.aqr.com/Insights/Research/White-Papers/Long-Only-Style-Investing)
: This paper propose multi-factor integrated portfolio building strategy. Since traditional multi-factor merely mix multiple factors, overall portfolio was close to suboptimal. But integrated multi factor portfolio shows better and optimal portfolio.

### (5) Value Momentum Everywhere
#### [paper](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2174501)
: This paper studies the returns to value and momentum strategies jointly across eight diverse markets and asset classes. Implication derived from empirical data from fixed income and credit market is led our research project to come up with advanced multi-factor asset pricing model.

### (6) Factor Zoo (.zip)
#### [paper](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4605976)
: This paper collects cross-sectional stock return analysis, which are proposed in asset pricing academia.  The paper explore how much this ‘factor zoo’ can be compressed, focusing on explaining the available alpha rather than the covariance matrix of factor returns and suggest that about 15 factors are enough to span the entire factor zoo. 

### (7) Taming the Factor Zoo
#### [paper](https://www.aqr.com/About-Us/AQR-Insight-Award/2018/Taming-the-Factor-Zoo)
: This paper propose

### (8) RETRACTED: Common risk factors in the cross-section of corporate bond returns☆
#### [paper](https://www.sciencedirect.com/science/article/pii/S0304405X18302095)
: This article has been retracted at the request of the authors. This article constructs risk factors based on the following characteristics of corporate bonds: downside risk, credit risk, and liquidity risk. The article shows that these factors have statistically significant risk premia and that they outperform other bond pricing models in explaining the returns of portfolios of corporate bonds sorted on industry, size, and maturity.

### (9) Priced Risk in Corporate Bonds
#### [paper](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4398449)
: This paper revisit recent findings of (8) and provide evidence that common factor pricing in corporate bonds is exceedingly difficult to establish. Based on portfolio- and bond-level analyses, we demonstrate that previously proposed bond risk factors, with traded liquidity as the only marginal exception, do not have any incremental explanatory power over the corporate bond market factor. Consequently, this implies that the bond CAPM is not dominated by either traded- or nontraded-factor models in pairwise and multiple model comparison tests.

### (10) Bond Portfolio Optimization Using Dynamic Factor Models
### [paper](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2079318)
: This paper proposes an application of dynamic factor models for bond portfolio optimization. By deriving closed-form expressions for expected bond returns and their covariance matrices, it facilitates optimal mean-variance bond portfolios, including a duration-constrained variant for bond indexing. 

### (11) Is 1/n Really Better than Optimal Mean-Variance Portfolio?   
### [paper](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2530287)   
: This paper evaluates the performance ranking of the 1/n portfolio in absolute sense. The author enumerate all possible portfolios within a specified asset universe, and compare the 1/n portfolio among all possible portfolios to find that 1/n is not really better than the average portfolio.