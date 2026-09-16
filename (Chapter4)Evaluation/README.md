# 4. Evaluation: diversification without reliable incremental alpha

[Portfolio construction](../%28Chapter3%29Porfrolio_model/README.md) · [Next: Applications](../%28Chapter5%29Application/README.md)

## Main result

The fixed combination of bond and equity-derived signals produces a **0.13% annual arithmetic mean** and **0.05 Sharpe** over September 2002–November 2021. Its market-plus-TERM alpha is **0.61% annually**, with p = **0.343** and BH q = **0.685**. The evidence does not establish positive alpha.

All estimates below are **computed in this repository**, using gross long–short factor returns. Published findings are separately attributed in the [source register](../research/SOURCES.md).

## Full sample: 231 months

| Strategy | Annual mean | Annual vol. | Sharpe | Annual alpha¹ | Alpha p | BH q |
|---|---:|---:|---:|---:|---:|---:|
| Bond-only | −0.12% | 3.47% | −0.03 | 0.54% | 0.539 | 0.770 |
| Equity-derived | 0.37% | 2.18% | 0.17 | 0.68% | 0.182 | 0.455 |
| Combined | 0.13% | 2.53% | 0.05 | 0.61% | 0.343 | 0.685 |
| Combined minus bond | 0.24% | 1.40% | 0.17 | 0.07% | 0.825 | 0.888 |

¹ MKTB + TERM regression; six-lag Newey–West covariance. Means and alphas are annualized arithmetically; p- and q-values are two-sided.

The direct improvement in mean return has p = **0.465**. Its annual alpha difference is **0.07%**, with a 95% interval of **−0.55% to +0.69%**. Neither comparison supports a reliable incremental benefit.

![Alpha estimates and uncertainty](../research/figures/alpha_intervals.png)

### Individual signals

| Signal | Annual mean | Sharpe | Annual alpha¹ | Alpha p | BH q |
|---|---:|---:|---:|---:|---:|
| Credit spread | 9.95% | 0.69 | 4.82% | 0.010 | 0.100 |
| Bond momentum | −1.96% | −0.17 | −0.87% | 0.758 | 0.888 |
| Low volatility | −8.34% | −0.78 | −2.35% | 0.150 | 0.455 |
| Equity momentum | 0.63% | 0.08 | 2.86% | 0.049 | 0.244 |
| Equity value | 0.92% | 0.12 | −0.95% | 0.421 | 0.701 |
| Equity profitability | −0.43% | −0.10 | 0.12% | 0.888 | 0.888 |

Credit spread has positive nominal alpha evidence, but does not pass the stated 5% BH threshold. None of the ten market-plus-TERM alpha tests passes that threshold. The negative low-volatility mean does pass the separate mean-test family; statistical significance need not indicate a profitable hypothesized direction.

## Chronological stability

| Segment | Dates | Months | Bond-only mean | Equity-derived mean | Combined mean |
|---|---|---:|---:|---:|---:|
| Development | Sep 2002–Jan 2016 | 161 | 0.07% | 0.70% | 0.38% |
| Evaluation | Feb 2016–Nov 2021 | 70 | −0.54% | −0.38% | −0.46% |
| Original-period overlap | Jan 2013–Nov 2021 | 107 | 0.42% | 0.20% | 0.31% |

The evaluation segment contains the final 30% of months, rounded upward. Definitions are fixed, but this is not an untouched out-of-sample discovery test: source data were retrospectively revised and the hypotheses came from published research.

The evaluation-period combined Sharpe is **−0.22** and alpha is **−0.41%**, p = **0.707**. The overlapping 2013-period comparison is a sensitivity check, not an independent validation sample.

## Source and methodology sensitivity

| Combined strategy, same dates | Full-sample mean | Full-sample Sharpe | Evaluation mean |
|---|---:|---:|---:|
| DFPS | 0.13% | 0.05 | −0.46% |
| OSBAP | 0.16% | 0.06 | −0.41% |
| ICE | 0.20% | 0.08 | −0.40% |
| ICE, duration-adjusted returns | 0.54% | 0.23 | −0.43% |

The first three hold the selected concepts and weights constant while changing the supplied return file. Their agreement is not three independent experiments: they share signals, issuers, calendar periods, and substantial underlying information. The duration-adjusted line changes the return definition and is not a TRACE duration hedge.

The full-sample combined alpha p-value remains above 0.30 with Newey–West bandwidths of 3, 6, and 12 months. Equal-versus-value-weighted security portfolios and realistic execution delays cannot be reconstructed from these aggregate inputs. Although the older archive contains a turnover file, it pertains to its source portfolios and does not establish turnover for the combined TRACE strategy after netting.

[Source comparisons and estimates](../research/results/performance.csv) · [Duration sensitivity](../research/results/duration_sensitivity.csv) · [Bandwidth sensitivity](../research/results/hac_sensitivity.csv)

## Costs and drawdowns

The combined portfolio's full-sample maximum cumulative P&L decline is **13.77% of fixed long-side notional**; the corresponding bond-only decline is 17.51%. These are not funded-NAV drawdowns.

| Assumed annual cost hurdle | Combined full-sample annual mean after hurdle |
|---|---:|
| 0 bps | 0.13% |
| 100 bps | −0.87% |
| 200 bps | −1.87% |
| 400 bps | −3.87% |

These deductions are **uncalibrated scenarios**, not measured transaction costs. The gross annual mean leaves only about **12.85 bps** before reaching zero; execution delays and borrow fees require separate measurement. [Scenario calculations](../research/results/cost_hurdles.csv)

## Validation and research boundary

The author-table reproduction covers 4,092 statistics. Seven targeted checks verify economic signs, missing-factor handling, ambiguous columns, portfolio arithmetic, initial-loss drawdown treatment, rank deficiency, and Newey–West covariance against an independent matrix calculation.

The analysis does not replicate every published table, prove market efficiency, estimate causal effects, or reject all equity information in credit. It rejects a strong investment claim for **this fixed six-signal combination under these data and definitions**. The resulting research conclusion is complete even though an executable security-level strategy has not been demonstrated.

[Exact outputs](../research/results/) · [Tests](../research/test_study.py) · [Combined notebook](../Combined_README.ipynb)
