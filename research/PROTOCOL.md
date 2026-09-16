# Research protocol

Initial specification dated 15 September 2026; exploratory amendment dated
16 September 2026. The initial document describes choices made before its performance
inspection, but this working tree supplies no independently timestamped preregistration.
The amendment follows inspection of the original results. Neither is a pristine
out-of-sample discovery test, and the amendment must not inherit that description.

## Exploratory amendment: incremental information and the allocation decision

The original six signals, directions, source archives, samples and 50/50 weights below
are retained. The following diagnostics are specified before computing their new
outputs, after the original findings were known. No winning signal or specification
will replace the original experiment. The intended audience is systematic credit
research; this is not a derivatives-pricing or live trading demonstration.

1. **Incremental information.** Does the equity-derived bond composite have positive
   alpha conditional on all three individual bond factors, MKTB and TERM? Estimate
   this regression for the composite and each equity-derived signal. The composite
   is the primary question; components diagnose it. Report full, development and
   evaluation segments in each of DFPS, OSBAP and ICE; use HAC bandwidths 3, 6 and 12
   with 6 primary. Report 95% pointwise intervals and BH q-values within each family
   of four targets/dataset/segment/bandwidth. This tests benchmark-relative alpha,
   not full mean-variance spanning, causal information flow or an executable hedge.
2. **Diversification versus less exposure.** Compare the unchanged combined return
   with bond-only and a bond-only control scaled by the preceding 60 months' ratio
   of combined to bond volatility, clipped to [0, 1]. Hold its weight for month t
   using only returns through t−1. Unused reference notional contributes zero excess
   P&L; this is not a funded cash allocation. Exclude the 60-month warmup from every
   comparator. Report the resulting realized volatilities and cap frequency: they
   need not match. Report both all post-warmup months and the original evaluation
   segment. Use paired circular-block bootstrap percentile intervals for Sharpe
   differences (5,000 draws, seed 20260916, blocks of 6 and 12 months). These are
   descriptive intervals conditional on realized paths and weights, assume useful
   within-period stationarity, and are not studentized hypothesis tests. Do not
   describe them as a replication of Ledoit–Wolf's test or as correcting selection.
3. **Cost budget and precision.** For combined-minus-each-control returns, report
   the annual mean in basis points with six-lag HAC intervals. This is incremental
   constant-cost headroom, not total strategy cost capacity or observed turnover.
   A negative estimate means no positive estimated additional-cost budget; do not
   clip negative estimates or interval bounds. Use 50 bps/year as an illustrative
   materiality threshold, chosen here for decision clarity, not calibrated costs.
   An interval spanning that threshold is inconclusive, not evidence of equivalence.
   Report an approximate 80%-power detectable effect of (1.96 + 0.8416) times the
   annualized HAC standard error, conditional on its estimated variance remaining
   applicable. It is a precision diagnostic, not a promised future sample size.
4. **Measurement sensitivity.** Compare the same combined monthly returns across
   each source pair with a paired six-lag HAC mean-difference interval. Use full
   and evaluation periods, and BH adjustment over the three pairs within a period.
   Shared dates, signals and inputs make these sensitivity checks dependent.

The decision is whether evidence warrants a new, point-in-time security-level study.
Positive in-sample alpha alone is insufficient. New execution data, issuer links,
dated information, risk controls and an untouched later sample are prerequisites
for any investability claim. No synthetic panel will substitute for them.

Amendment outputs: `incremental_spanning.csv`, `risk_control_returns_*.csv`,
`risk_control_performance.csv`, `sharpe_difference_intervals.csv`,
`incremental_cost_budget.csv`, `paired_source_differences.csv`, and
`incremental_metadata.json` in `research/results/`. They regenerate through
`uv run python research/run_study.py` from the same cached, hash-verified archives;
rerunning overwrites derived artifacts, not raw sources. No network is needed.

## Question and selection

Do issuer equity signals add information to corporate bond signal portfolios?
The six concepts are bond credit spread (+), bond momentum (+), bond low volatility
(− on volatility), issuer equity momentum (+), equity book-to-market (+), and equity
profitability (+). Exact column mappings will follow the authors' definitions, not
the observed returns. Missing concepts are excluded without performance-based replacement.

The primary data are author-released, value-weighted long–short corporate bond factor
returns from the July 2025 alternative-database archive. TRACE is the primary return
source; ICE-based results are a source sensitivity check. The November 2024 archive
provides additional definitions/weighting comparisons where compatible. No claim of
having independently cleaned transaction-level TRACE data is made.

Before computing performance, the primary return file was fixed to DFPS (the corrected
TRACE source); OSBAP and ICE were retained as alternatives. Source inspection mapped
the six concepts to VW_18_spread, VW_12_mom6, VW_27_volatility, VW_ret_6_1, VW_be_me,
and VW_gp_at. Starred columns were inverted to recover high-minus-low direction, then
the volatility factor was inverted to implement the low-volatility hypothesis. No
signal was substituted. The December 2025 co-pricing bundle supplies MKTB and TERM.

Feasibility resolution: the numerical archives support value-weighted factor-series
analysis and an ICE duration-adjusted sensitivity. They do not support a new security-level
integrated portfolio or an equal-weighted security comparison. Those analyses are not
claimed; no missing panel values or holdings are inferred. Source-provided turnover is
not used to claim netted turnover of the combined TRACE strategy.

## Comparisons

Average available bond sleeves equally, average available equity-derived bond sleeves
equally, and average the two composites 50/50. All remain bond long–short strategies;
none includes a direct equity allocation. No optimized or performance-selected weights.
Use the common contiguous monthly sample for primary comparisons and the final 30%
of months (ceiling) as a chronological evaluation segment. Definitions are fixed before
inspection, but these published signals and revised historical data are not an untouched
out-of-sample discovery experiment. Also report the intersection with 2013–2023.

Report annualized arithmetic means, sample volatility, Sharpe ratios, cumulative
factor P&L, normalized-notional drawdowns, correlations, and six-lag Newey–West inference.
Use bond-market alpha and bond-market-plus-Treasury alpha if a public benchmark with
documented return units and timing is available. Use separate BH families for mean and
alpha tests of the selected signals, composites, and combined-minus-bond comparison.
The return difference directly tests improvement in average return; a higher Sharpe ratio
alone does not establish a statistically significant improvement.

## Interpretation constraints

Check source sign corrections before combining factors. Economic directions must not
be inferred from sample means. If source signs cannot be recovered, report the gap and
do not describe sign-selected performance as prospective evidence.
Factor return files do not identify holdings, turnover, issuer concentration, execution
prices, or costs. Any annual cost deduction is a labeled hurdle scenario. Security-level
terciles and issuer balancing require suitable public panel data and identifier/timing
validation; do not manufacture them from aggregate returns.

## Recovery and outputs

Run `python3 research/download_sources.py` to cache archives in `research/data/raw/`.
Completed downloads are reused and hashes verified; interrupted `.partial` downloads
restart. `source_manifest.json` records provenance. Analysis will write derived CSVs
under `research/results/` and figures under `research/figures/`; these can be regenerated
from the cached archives. Existing research scripts and historical outputs are preserved.
