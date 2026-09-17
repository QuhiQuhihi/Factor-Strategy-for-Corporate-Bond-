# 2. Factors: replication before interpretation

[Data](01-data.md) · [Next: Portfolio construction](03-portfolios.md)

## Research hypotheses

The main question is **whether issuer equity information adds positive conditional
alpha beyond existing bond signals**. A portfolio average alone cannot answer this:
it can conceal offsetting signals and changes in risk. The initial hypotheses remain:

1. Credit spreads, past bond returns, and bond volatility may capture different credit exposures.
2. Issuer equity momentum, valuation, and profitability may contain information relevant to creditors.
3. Combining the groups may improve diversification and incremental performance.

These are hypotheses, not assertions that high characteristic values always earn higher returns. A characteristic is an input used to sort securities; a factor return is the return of that sorted portfolio; a regression beta is its estimated exposure to another return series. The study keeps these objects separate.

## Six fixed signals

| Signal | Source column in primary archive | Characteristic | Chosen long side | Multiply stored return by |
|---|---|---|---|---:|
| Credit spread | VW_18_spread | Bond option-adjusted spread | Higher spread | +1 |
| Bond momentum | VW_12_mom6* | Prior six-month bond return sum, excluding most recent month | Past winners | −1 |
| Low volatility | VW_27_volatility | Rolling bond-return volatility | Lower volatility | −1 |
| Equity momentum | VW_ret_6_1 | Issuer equity price momentum, excluding most recent month | Past winners | +1 |
| Equity value | VW_be_me | Issuer book equity / market equity | Higher book-to-market | +1 |
| Equity profitability | VW_gp_at* | Issuer gross profits / assets | More profitable issuers | −1 |

Bond definitions follow [Factor Investing with Delays, Table A.1](https://www.ier.hit-u.ac.jp/Common/publication/DP/DPS-A771.pdf). Volatility uses a window expanding from 12 observations to 36. Equity definitions follow [Global Factor Data documentation](https://jkpfactors-data.s3.amazonaws.com/documents/Documentation.pdf), including ret_6_1, be_me, and gp_at.

The [initial protocol](../research/PROTOCOL.md) records these concepts and economic
directions; no independently timestamped preregistration is established by this working
tree. Low volatility is a deliberately tested defensive hypothesis, not a recommendation
to reverse the observed high-volatility premium. The 16 September diagnostics were
added after the original results were inspected and are explicitly exploratory.

### Recovering factor direction

An asterisk marks a factor flipped by the provider to produce a positive historical premium. For the economic-direction study:

~~~math
f^{economic}_{j,t}=d_j s_j f^{stored}_{j,t},
\qquad s_j=-1\text{ for starred columns, }+1\text{ otherwise}.
~~~

Here d is +1 for a high-minus-low characteristic strategy and −1 for low volatility. Low volatility reverses an unstarred high-volatility return; bond momentum and profitability undo starred reversals. The machine-readable [mapping](../research/results/signal_mapping.csv) makes both operations explicit. The [provider documents the sign convention](https://openbondassetpricing.com/machine-learning-data/).

This choice matters: the combined portfolio's source-oriented mean is 3.71% annually and Sharpe is 0.66; the economic-direction version has a 0.13% mean and 0.05 Sharpe. These portfolios differ in their actual exposures. The comparison does not isolate all forms of look-ahead bias or establish that every source factor is biased.

## What is reproduced

The July 2025 archive includes DatabaseComparison_DNR_2022.csv and database_comparison.py. I independently recompute its 341-factor comparison: three correlations, three monthly means, three annualized Sharpe ratios, and three paired-test p-values for each factor.

**All 4,092 values match, with maximum absolute error 7.22 × 10⁻¹⁶.** This validates reproduction of the archived summary table, not the original transaction-level construction.

| Stored factor | Reported monthly mean | Recomputed monthly mean | Reported / recomputed Sharpe |
|---|---:|---:|---:|
| Credit spread | 0.829182% | 0.829182% | 0.688813 / 0.688813 |
| Bond momentum* | 0.163064% | 0.163064% | 0.174137 / 0.174137 |
| High volatility | 0.695125% | 0.695125% | 0.784686 / 0.784686 |
| Equity momentum | 0.052435% | 0.052435% | 0.079462 / 0.079462 |
| Equity value | 0.076900% | 0.076900% | 0.122507 / 0.122507 |
| Equity profitability* | 0.036093% | 0.036093% | 0.095786 / 0.095786 |

*DFPS, September 2002–November 2021, authors' stored orientation. The replication retains the authors' paired iid t-tests; the extension uses HAC inference. [Exact comparison](../research/results/replication_selected.csv)*

## How the literature informs this study

The [source register](../research/SOURCES.md) separates published findings from calculations performed here.

- **Priced Risk in Corporate Bonds:** corrected temporal alignment weakens several established factors' incremental pricing evidence. This motivates an explicit market benchmark.
- **Corporate Bond Factors: Replication Failures and a New Framework:** reports surviving bond and equity-derived signals under its construction. This motivates studying issuer information, without assuming that all equity styles transfer.
- **Factor Investing with Delays:** studies how infrequent execution affects factor economics. This prevents equating gross factor performance with implementable alpha.
- **The Corporate Bond Factor Replication Crisis:** examines shared-price measurement error, future-dependent filtering, and construction sensitivity. This motivates transparent signs, fixed definitions, and source comparisons.
- **The Co-Pricing Factor Zoo:** studies a substantially larger joint bond/equity pricing model. This six-signal strategy does not reproduce or contradict that model merely by producing a weak result.

## Estimation

For each of the six signals, three composites, and the combined-minus-bond contrast:

~~~math
f_t=\alpha+\beta_M MKTB_t+\varepsilon_t,
\qquad
f_t=\alpha+\beta_M MKTB_t+\beta_T TERM_t+\varepsilon_t.
~~~

OLS uses the full stated sample or segment, with Newey–West covariance, six lags, Bartlett weights, and the n/(n−k) finite-sample adjustment. Tests use the asymptotic normal distribution. Confidence intervals are pointwise 95% intervals.

Benjamini–Hochberg q-values are computed separately for ten mean tests, ten market-alpha tests, and ten market-plus-TERM-alpha tests within each dataset/segment. Correlated factors and multiple sensitivity exercises mean these are defined-family adjustments, not a universal correction for all research choices.

The regressions check that observations are sufficient and the design matrix has full rank.

## New question: incremental information conditional on bond factors

For each equity-derived bond factor and their equal-weight composite, estimate:

~~~math
E_{j,t}=\alpha_j+\gamma_{1j}f_{spread,t}+\gamma_{2j}f_{bondmom,t}
+\gamma_{3j}f_{lowvol,t}+\beta_{Mj}MKTB_t+\beta_{Tj}TERM_t+\epsilon_{j,t}.
~~~

The composite is the primary target; the three components explain its result.
The mechanism hypothesis is that issuer information contains credit-relevant variation
beyond these bond portfolios. A nonzero intercept is conditional evidence against this
particular linear return model, not proof of the mechanism, complete mean-variance
spanning, or a pricing error in an individual bond. Contemporaneous regression
coefficients are estimated in each stated sample; they are not a feasible trading rule.

The [amendment](../research/PROTOCOL.md) fixes HAC lags 6, with 3 and 12 as sensitivity
checks; full, development, and evaluation segments; and all three return sources.
BH families contain the four targets within each dataset/segment/bandwidth. The
composite overlaps its components, so these are dependent diagnostics. No correction
for all prior research choices is claimed.

The [results](../research/results/incremental_spanning.csv) include intervals, p- and
q-values, R², residual volatility, and a condition number after standardizing controls.
Full-sample DFPS conditional alphas are 3.93% for equity momentum, −2.33% for value,
and 0.20% for profitability; their average is the composite's 0.60%. The economic
directions and original portfolio weights remain unchanged. A negative value estimate
does not authorize turning it into a successful short-value strategy after inspection.
