## Defining Factors for our model
Using data from previous chapter, we continoued our research about which factor is significant in explainaing corporate bond's return recently. 

AQR's paper examine Investment Grade (Moodys AAA to A-), Investment Grade Minus (Moodys BBB+ to BBB-), and Junk Grade (Moodys BB+ and below). However our project mainly focuss on Investment Grade and Investment Grade Minus (Moodys AAA to BBB-), which are commonly classified as investment grade. 

And we are going to examine each bond with factor $i$. So, compute $r_{t, i}$  for each signal $i$ at time $t$. And we assume that there are High, Mid, Low segments. This allow us to cover 67% of our universe, which incorporate broader and more extreme values into our model than Factor Zoo project. Equation for calculating each factor $i$ follows : 

 $f_{t,i} = r_{t,high-i} - r_{t,low-i}$
This means that we buy high factor (Top 33%) and sell short factor (low 33%).

First, we use valueweighted returns since this makes the factors more implementable than equal-weighting and
reduces issues with missing values. Second, we use tertile portfolios, i.e., sort into three groups, since this uses two-thirds of the data, rather than the more extreme decile portfolios often used in the literature that only uses 20% of the data. Also, we use monthly rebalancing to condition on the most up-to-date information.

This factors (premiums) will be multiplied with coefficient and sumed up. In here, coefficient will be derived by regression fitting. Total sum will be compared with each cusip's return.

## How to examine each factors
a robust and consistent method for constructing all long-short factor returns, in addition to our clean data. 

$f_{t,i} = \alpha_i + \beta_{CMKT} * CMKT_{t} + \beta_{TERM} * TERM_{t} + \epsilion_t$

$f_{t,i} = \alpha_i + \beta_{CMKT} * CMKT_{t} + \beta_{TERM} * TERM_{t} + \beta_{factor i} * FACTOR_i + \epsilion_t$


## What is Benchmark Model
Like Famma-French Model or CAPM model, we can use very simple market data driven model to examine the power of mullti-facator model.
