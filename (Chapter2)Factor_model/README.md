## Defining Factors for our model
Using data from previous chapter, we continoued our research about which factor is significant in explainaing corporate bond's return recently. Market factors, Firm level factors, Security level factors are included in multi factor model. Explanation about each factors are elaborated in appendix.

AQR's paper examine Investment Grade (Moodys AAA to A-), Investment Grade Minus (Moodys BBB+ to BBB-), and Junk Grade (Moodys BB+ and below). However our project mainly focuss on Investment Grade and Investment Grade Minus (Moodys AAA to BBB-), which are commonly classified as investment grade. 

## Regression based factors model
To isolate the unique returns attributed to specific factors independent of overall market movements, the study employs a regression model where factor returns are regressed against a composite of the corporate bond market and Treasury bond returns. The model is formalized as follows:

#### $f_{t,i} = \alpha_i + \beta_{CMKT} * CMKT_{t} + \beta_{TERM} * TERM_{t} + \epsilon_t$

#### $f_{t,i} = \alpha_i + \beta_{CMKT} * CMKT_{t} + \beta_{TERM} * TERM_{t} + \beta_{factor i} * FACTOR_i + \epsilon_t$


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

