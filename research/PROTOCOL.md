# Research protocol

Specified before inspecting factor performance, 15 September 2026.

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
