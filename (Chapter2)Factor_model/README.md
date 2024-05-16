## Defining Factors for our model
Using data from previous chapter, we continoued our research about which factor is significant in explainaing corporate bond's return recently. Market factors, Firm level factors, Security level factors are included in multi factor model. Explanation about each factors are elaborated in appendix.

AQR's paper examine Investment Grade (Moodys AAA to A-), Investment Grade Minus (Moodys BBB+ to BBB-), and Junk Grade (Moodys BB+ and below). However our project mainly focuss on Investment Grade and Investment Grade Minus (Moodys AAA to BBB-), which are commonly classified as investment grade. 

## Regression based factors model
To isolate the unique returns attributed to specific factors independent of overall market movements, the study employs a regression model where factor returns are regressed against a composite of the corporate bond market and Treasury bond returns. The model is formalized as follows:

#### $f_{t,i} = \alpha_i + \beta_{CMKT} * CMKT_{t} + \beta_{TERM} * TERM_{t} + \epsilon_t$

#### $f_{t,i} = \alpha_i + \beta_{CMKT} * CMKT_{t} + \beta_{TERM} * TERM_{t} + \beta_{factor i} * FACTOR_i + \epsilon_t$

## Multi Regression based factor model
To enhance explanatory power beyond term premium and market premium, multiple factors are included in this project. Following is 11 additional factors used in our model. Term and market factors are included as base model.   
- Duration : Modified Macaulay duration [(12)]
- Credit Spread :  Yield to maturity minus the yield on a cash-flow matched portfolio of treasuries [(12)]
- Yield To Maturity : Promised yield to maturity [(12)]
- Volatility :  36 month vol [(8)]
- Skewness :  36 month skew [(8)]
- 3 month momentum : 3 month momentum [(14)]
- 6 month momentum : 6 month momentum [(14)]
- Price to book ratio :  Bond book value / market price [(12)]
- Default beta :  The regression coefficient on DEF in a rolling regression of bonds excess return on the default factor [(13)]
- Value at Risk (10%) : -1 * 4th lowest observation in a 36 month rolling window [(8)]
- Equity Momentum :  6 month equity momentum [(14)] [(13)]  

## Minor issue with data and quant model
In the academic context of fixed income securities, the observed premium of on-the-run (OTR) bonds over off-the-run (OTR) bonds is a well-documented phenomenon, often attributed to liquidity differences and demand disparities between the two types of bonds.

#### Liquidity Premium: 
On-the-run bonds, being the most recently issued and therefore most current series of a government's debt, typically exhibit higher liquidity compared to off-the-run bonds. This higher liquidity is manifested in narrower bid-ask spreads and greater ease of trading, which is highly valued by market participants. As a result, investors are willing to accept a lower yield on OTR bonds, translating into a price premium over older, less liquid off-the-run bonds.

#### Demand Dynamics:
 On-the-run bonds also benefit from structural demand driven by benchmarking and portfolio rebalancing. Many institutional investors, such as pension funds and insurance companies, as well as investment benchmarks, prefer or require the most current issue of a bond series for their portfolios. This structural demand increases the price of on-the-run bonds, further contributing to their premium.   

Our model use past 8 month data to evaluate new issued security. THis means that we are targeting off-the-run bond only. It would be great we can use quant model right after the bond is issued. Since this project is asset pricing project, we are going to use this naive model with potential issue.

## Building long-short factor construction
And we are going to examine each bond with factor $i$. So, compute $r_{t, i}$  for each signal $i$ at time $t$. And we assume that there are High, Mid, Low segments. This allow us to cover 67% of our universe, which incorporate broader and more general trends (besides outlier in dirty datasets) values into our model than Factor Zoo project. Equation for calculating each factor $i$ follows : 
#### $r_{t,i} = r_{t,high-i} - r_{t,low-i}$   
This means that we buy high factor (Top 33%) and sell short factor (low 33%). 

## Multiple Testing Corrections
Given the multiple hypotheses tested in identifying significant factors, a multiple testing correction is applied using the Benjamini-Hochberg procedure. This adjusts the false discovery rate, particularly important in the context of multiple comparisons. The adjusted significance level for a test statistic $t_i$ is determined based on its ranking r among all tested hypotheses 𝑁:
#### Adjusted $p_i$ = $min(1,p_i * (N/r))$
where $p_i$ is the p-value associated with $t_i$.   

## What is Benchmark Model
Like Famma-French Model or CAPM model, we can use very simple market data driven model to examine the power of mullti-facator model. 

