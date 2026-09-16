# 1. Data: a TRACE return study with explicit source boundaries

[Overview](../README.md) · [Next: Factors](../%28Chapter2%29Factor_model/README.md)

## The empirical unit

The current study observes **monthly long–short bond factor returns** supplied by external researchers. Each column represents a portfolio formed from a bond or issuer characteristic. Rows contain decimal returns at month-end: 0.01 means 1%.

This unit supports factor replication, combination, risk regressions, and time-series inference. It does not reveal each bond's holdings, point-in-time eligibility, transaction price, or issuer exposure.

## Sources and coverage

| Input | Available period | Monthly rows | Role |
|---|---|---:|---|
| ExcessLongShortVW_DFPS.csv | Sep 2002–Nov 2021 | 231 | Primary TRACE-derived return series |
| ExcessLongShortVW_OSBAP.csv | Sep 2002–Sep 2022 | 241 | Alternative source sensitivity |
| ExcessLongShortVW_ICE.csv | Aug 2002–Nov 2022 | 244 | ICE return-source sensitivity |
| DurAdjLongShortVW.csv | Restricted here to the common period | 231 used | Separate ICE duration-adjusted comparison |
| traded_bond_excess.csv: MKTB, TERM | Jan 1986–Dec 2022 | 444 | Public market and Treasury benchmark series |

The first three files contain the same 341 signal names and are distributed with an [author comparison script and reference table](https://openbondassetpricing.com/wp-content/uploads/2025/07/ExcessLongShortVW_All_Databases.zip). The DFPS label identifies Dick-Nielsen, Feldhütter, Pedersen, and Stolborg's return source. The archive's labels are retained throughout the result tables.

The characteristics are not all constructed from TRACE. The provider documents ICE/BAML bond predictors and equity characteristics from Open Source Asset Pricing and Global Factor Data. Thus **TRACE-derived returns paired with externally constructed signals** describes this study more precisely than “a pure TRACE strategy.” [Provider documentation](https://openbondassetpricing.com/machine-learning-data/)

The separate [co-pricing archive](https://openbondassetpricing.com/wp-content/uploads/2025/12/djm_data.zip) supplies MKTB, the corporate bond market excess return, and TERM, a long-government-bond return less the one-month bill rate. These are published benchmark series, not a market index reconstructed from the DFPS investment universe. Their definitions are in [The Co-Pricing Factor Zoo, Appendix A](https://arxiv.org/html/2604.04430v1#A1).

## Sample construction

The primary comparison uses the intersection of all six selected signals, all three return sources, and both benchmarks:

- Full sample: **September 2002–November 2021, 231 months**.
- Development segment: September 2002–January 2016, 161 months.
- Final chronological evaluation: February 2016–November 2021, 70 months.
- Original-project period overlap: January 2013–November 2021, 107 months.

No 2022–2023 primary results are implied. Comparisons use identical dates. There is no missing-value imputation, return clipping, or selection based on observed profitability.

## Checks performed

[Data-quality results](../research/results/data_quality.csv) record zero duplicate months and zero missing observations in the six selected series for every source. The full archives do contain missing values: 257 cells for DFPS, 252 for OSBAP, and 251 for ICE. Those observations are handled pairwise in the author-table replication; they never enter the balanced six-signal study.

The analysis verifies:

- Month-end dates, unique months, and a contiguous common sample.
- Finite observed returns and the presence of each expected signal.
- Source checksums against the [download manifest](../research/data/source_manifest.json).
- Exact author-table replication, before changing factor orientation.
- Consistent orientation restoration independently for each file, including duration-adjusted factors.

Large returns remain in the sample. The study does not independently certify the quality of every underlying bond transaction.

## What cannot be inferred

The factor files do not permit rebuilding issuer-balanced portfolios, an investment-grade-only universe, or rating/duration-neutral holdings. Public bond panels also omit proprietary fields such as ratings and GVKEYs; the predictor panel requires a separate bond-return merge. [Public panel scope](https://openbondassetpricing.com/data/)

The completed empirical scope therefore uses factor series. Security-level tercile construction remains an extension requiring matched identifiers, point-in-time signals, and eligible returns. No claim of security-level replication is made.

## Relation to the original data work

The earlier scripts depended on TRACE.db and Windows paths. The inspected bond-return routine adds a monthly coupon approximation to prices, forward-fills observations, and contains a shift outside the bond grouping and inconsistent outlier code. This is not sufficient evidence of correct accrued-interest total returns.

For a future security-level reconstruction, total return must account separately for beginning and ending accrued interest and actual cash payments:

~~~math
R_{i,t+1} =
\frac{P_{i,t+1}+AI_{i,t+1}+C_{i,t+1}}{P_{i,t}+AI_{i,t}}-1.
~~~

The current analysis consumes authors' portfolio returns and does not run that legacy calculation. TRACE is operated by FINRA; the former “TRACE database by SEC” description was inaccurate. [FINRA TRACE](https://www.finra.org/filing-reporting/trace)

## Files and recovery

[download_sources.py](../research/download_sources.py) caches three numerical archives in research/data/raw/. Those files are ignored by Git. [run_study.py](../research/run_study.py) generates the balanced return panels and statistical outputs. All derived returns remain decimal; displayed percentages are explicitly labeled.

Rerun the downloader after an interrupted transfer; it restarts the partial archive and retains completed files. Rerun the analysis from the cached files to regenerate results. Optional paper caches use the downloader's --references flag. The [source register](../research/SOURCES.md) records the publications and precise evidence used.
