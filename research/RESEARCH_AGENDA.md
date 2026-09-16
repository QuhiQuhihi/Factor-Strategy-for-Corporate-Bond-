# Next research experiments

The completed factor-level study motivates the experiments below. They are designed,
not run; each requires a matched security panel and new validation data.

## Highest-priority new experiment: information transmission or stale prices?

**Question:** Does issuer equity momentum predict subsequent bond excess returns
within comparable credit-risk groups, or does the apparent effect reflect common risk
and delayed bond-price observation?

**Mechanism to test:** Equity markets may incorporate issuer news before some bond
prices adjust. **Competing explanations:** credit-risk exposure, distress, stale marks,
and an untradeable entry price. The existing factor-level intercept cannot choose
among these explanations. The conditional momentum result motivates this question
after inspection; it is not fresh confirmatory evidence for it.

| Design element | Concrete requirement before inspecting a new evaluation sample |
|---|---|
| Population | Define eligible USD fixed-rate corporate bonds, price-age eligibility, issuer coverage and exclusions; retain defaults, calls and exits |
| Information set | Point-in-time issuer links, equity prices and accounting publication dates; a source vintage and actual availability timestamp for each input |
| Signal | Retain the existing issuer equity momentum definition; residualize within training data against disclosed credit-risk characteristics; never choose the sign from outcomes |
| Comparison | Same bonds/dates for bond-only and bond-plus-equity models, with issuer caps and comparable industry, rating, duration and spread exposures |
| Estimation | Chronological training and validation; issuer-grouped cross-sectional dependence; time-aware uncertainty and purging for overlapping targets |
| Timing diagnostic | Compare one-month-ahead excess returns using first executable prices after formation and alternative entry delays of 1 and 5 trading days; estimate returns from those entry prices |
| Liquidity diagnostic | Test whether the effect concentrates in old/stale observations and whether it survives a defined fresh-price subset; show coverage and selection differences |
| Economics | Record dirty prices, cash flows, default/recovery events, actual holdings, turnover, side-aware execution and borrowing/financing assumptions |
| Decision | Freeze a primary endpoint and economically justified minimum benefit before accessing the new holdout; require uncertainty, risk and cost evidence together |

An issuer equity signal is constant across that issuer's bonds at a given time.
Issuer-by-month fixed effects would absorb it. Use **cross-issuer comparisons within
risk groups** for this question; use within-issuer comparisons for maturity- or
bond-specific dislocations, which are a different hypothesis.

Shifting an aggregate factor-return series by one month does not simulate delayed
execution. A holdings-aware reconstruction must use the original formation decisions
and the later executable entry prices. Data ending in 2021 cannot test persistence
through the subsequent rate environment.

**Status: designed, not run.** Missing prerequisites are a matched point-in-time
security panel, sufficiently detailed execution observations, borrow information,
and an uninspected later sample. The present repository supplies none of those by
inference. Its existing cached inputs fully support the completed factor diagnostics.

## A second direction for a bank credit desk

**Question:** Do relative spread dislocations between bonds of the same issuer
predict convergence after matching cash flows, duration, seniority and embedded options?
This isolates a bond-level relative-value question rather than issuer equity news.
Compare residual spreads to an issuer curve estimated using only information then
available; test subsequent hedged P&L, entry delay, bid–ask bounds, and issuer clusters.
It needs security terms, yield curves, dirty prices and hedges. It is a proposed
extension, not another unexecuted module added to the current research pipeline.

