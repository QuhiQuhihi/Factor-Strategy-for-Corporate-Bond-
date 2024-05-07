# Multi Factor Model for Corporate Bond
This research project is to build multi-factor model and optimization tools for corporate bond (credit market) market using empirical data. Traditional factor models including value-momentum showed explanability in asset pricing model across various asset classes. [(5)](https://www.aqr.com/Insights/Research/White-Papers/Long-Only-Style-Investing). Ever since CAPM and Famma French factor model are introduced, there were a lot of attempts to explain equity return and collective study proved that these risk factors are eithter useful, useless, or redundant to span cross-sectional equity return. [(6)]((https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4605976)

Unlike equity market, there are not so many attempts to breakdown risk premium of credit bonds. Prominent research by Bai, Bali and Wen (2019) [(8)](https://www.sciencedirect.com/science/article/pii/S0304405X18302095) suggested common risk factors in cross-sectional return of corporate bond marekt. However, this research is retracted from Journal of Financial Econometrics in 2023 as subsequent research conducted by Dickerson, Mueller and Robotti (2023) [(9)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4398449) using a similar dataset of corporate bond returns reveals an error present in the data used by Bai et al. (2019) that consists of temporal misalignment of different data series.

 When expanding multi factor asset pricing model into fixed income market, the market shows its inherit incompleteness and proves multiple risk premium. For example, it is possible for one company to issue various bonds by setting differnt maturity, covenant, and collateral while there is one type of equity (besides prefered equity) This makes traders in credit market to consider multiple aspects with limited data. Also, structures embedded in fixed income securities, such as trench and secured, make valuation and execution difficult.  


## [Chapter 1 About Data](https://github.com/QuhiQuhihi/Factor-Strategy-for-Corporate-Bond-/tree/main/data)
This section discuss data used in this project. TRACE data from SEC and Financial Ratio from WRDS are used to build factor models. Since it is regulatory requirement to report corporate bond trade, a lot of insight about market can be found in this paper. However, complexity of data strucuture and cleaness makes huddle to implement asset pricing model in corporate bond strucuture. 

First of all, corporate bond data are more complex for several reasons: (i) whereas each company has a single stock, a company can have more than 100 bonds outstanding, (ii) the set of outstanding bonds changes over time, and (iii) some bond series are highly illiquid and the raw data have numerous erroneous and real outliers. 

In addition, addressing these data challenges was one of the key issue in our project. The project applied filters that eliminate a range of known errors, and then analyze all the most extreme remaining outliers “by hand,” eliminating errors and retaining extreme returns that represent real economic events. This process assures that we secure high level of integrity data for our model.

Lastly, WRDS database, which is most well known and widely used among academic researchers, is used for corporate level data. We didn't examine the integrity and adopted to our model.

Considering above points, the project completed building our dataset for asset pricing model. Detail about this database structure will be discussed in link above.

## [Chapter 2 Simple Factor Model for credit](https://github.com/QuhiQuhihi/Factor-Strategy-for-Corporate-Bond-/tree/main/(Chapter2)Factor_model)
This section reveals explanability and predictability of factors in credit market. Factor Zoo project examines factor models using empirical data and AQR project shows different result. Our project consider attractability for real-world investors to use this simplified approach. Same empirical data sets (TRACE, WRDS) are used to build factor model.

## [Chapter 3 Portfolio for credit](https://github.com/QuhiQuhihi/Factor-Strategy-for-Corporate-Bond-/tree/main/(Chapter3)Portfolio_model)

## [Chapter 4 Evaluating Performance](https://github.com/QuhiQuhihi/Factor-Strategy-for-Corporate-Bond-/tree/main/(Chpater4)Evaluation)

## [Chapter 5 Possible Application](https://github.com/QuhiQuhihi/Factor-Strategy-for-Corporate-Bond-/tree/main/(Chapter5)Application)
## Reference 

### (1) The Corporate Bond Factor Zoo
####[link](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4589786)
####[data](https://openbondassetpricing.com/)
: This paper propose explanability of corporate bond return using various factors in bond, equity, macro, and fundamental data. 

### (2) AQR Corporate Bond Factors: Replication Failures and a New Framework
#### [link](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4586652)  
#### [link](https://www.stolborg.com/data)
: This paper deal with replication failure of Corporate Bond Factor Zoo by Dickerson, Alexander and Julliard, Christian and Mueller, Philippe, The Corporate Bond Factor Zoo (October 2, 2023). 

### (3) Vanguard’s portfolio construction framework
#### [link](https://corporate.vanguard.com/content/dam/corp/research/pdf/vanguards_portfolio_construction_framework.pdf)
: This paper propose basic investing priciples and corresponding custom portfolio building. Our project review whether our proposed poftfolio strategy follows this protocol.

### (4) Long-Only Style Investing: Don't Just Mix, Integrate 
#### [link](https://www.aqr.com/Insights/Research/White-Papers/Long-Only-Style-Investing)
: This paper propose multi-factor integrated portfolio building strategy. Since traditional multi-factor merely mix multiple factors, overall portfolio was close to suboptimal. But integrated multi factor portfolio shows better and optimal portfolio.

### (5) Value Momentum Everywhere
#### [link](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2174501)
: This paper studies the returns to value and momentum strategies jointly across eight diverse markets and asset classes. Implication derived from empirical data from fixed income and credit market is led our research project to come up with advanced multi-factor asset pricing model.

### (6) Factor Zoo (.zip)
#### [link](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4605976)
: This paper collects cross-sectional stock return analysis, which are proposed in asset pricing academia.  The paper explore how much this ‘factor zoo’ can be compressed, focusing on explaining the available alpha rather than the covariance matrix of factor returns and suggest that about 15 factors are enough to span the entire factor zoo. 

### (7) Taming the Factor Zoo
#### [link](https://www.aqr.com/About-Us/AQR-Insight-Award/2018/Taming-the-Factor-Zoo)
: This paper propose

### (8) RETRACTED: Common risk factors in the cross-section of corporate bond returns☆
#### [link](https://www.sciencedirect.com/science/article/pii/S0304405X18302095)
: This article has been retracted at the request of the authors. This article constructs risk factors based on the following characteristics of corporate bonds: downside risk, credit risk, and liquidity risk. The article shows that these factors have statistically significant risk premia and that they outperform other bond pricing models in explaining the returns of portfolios of corporate bonds sorted on industry, size, and maturity.

### (9) Priced Risk in Corporate Bonds
#### [link](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4398449)
: This paper revisit recent findings of (8) and provide evidence that common factor pricing in corporate bonds is exceedingly difficult to establish. Based on portfolio- and bond-level analyses, we demonstrate that previously proposed bond risk factors, with traded liquidity as the only marginal exception, do not have any incremental explanatory power over the corporate bond market factor. Consequently, this implies that the bond CAPM is not dominated by either traded- or nontraded-factor models in pairwise and multiple model comparison tests.

