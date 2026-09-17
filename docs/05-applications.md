# 5. Applications: what the evidence supports

[Evaluation](04-evaluation.md) · [Overview](../README.md)

## Research conclusion

The fixed combination does not justify an allocation: it has inconclusive incremental
performance and a negative later mean before costs. The new conditional analysis
identifies a distinction hidden by the average: equity momentum has positive alpha
against the specified bond-factor controls, while equity value has negative alpha.
This is a lead for research, not a tested momentum-only investment strategy.

The useful output is a documented method for deciding whether an apparent credit factor deserves further investigation. It can support research prioritization and risk analysis; it does not yet justify deploying this portfolio.

## Practical uses

### Factor due diligence

Start by reproducing a provider's own statistics. Then inspect its sign conventions, information dates, weighting, return definition, and universe. This project reproduces the source table exactly, yet obtains a much lower combined Sharpe after applying the originally hypothesized directions.

That distinction matters when evaluating a proposed signal: a reproducible historical premium can still depend on an economically different trade or an infeasible construction.

### Credit exposure analysis

Credit spreads and low volatility largely offset in the tested portfolios. Equal signal weights therefore offer an incomplete picture of risk. A portfolio researcher can use the factor correlation matrix and market/TERM regressions as diagnostics before imposing bond-level duration, spread, rating, and issuer constraints.

The regression alpha is conditional on the selected benchmark. It is not a valuation estimate for an individual illiquid bond.

### Equity information in bond research

Issuer equity momentum, valuation, and profitability should not be treated as
interchangeable additions. Equity momentum's original market-plus-TERM alpha has
p = 0.049 and q = 0.244. In the exploratory model that additionally controls for the
three individual bond factors, its annual alpha is 3.93% with q = 0.00018; later
alpha is 2.91% with q = 0.010. These are different conditioning sets and testing
families. The composite's conditional alpha remains inconclusive. A contemporaneous
regression intercept does not establish net returns to a feasible hedge.

Future work should distinguish information about improving issuer fundamentals from compensation for changing credit risk. Bond and equity claims occupy different positions in the capital structure, so an equity-style label alone does not determine the appropriate credit trade.

## Research decision

Do not promote the fixed six-signal combination as a successful strategy. Its later
incremental mean versus the volatility-scaled bond control is −13.71 bps/year, with
a 95% interval ending at +24.19 bps. That provides no support for the amendment's
illustrative 50-bps additional-return requirement under the stated assumptions.

Allocate the next research effort to a narrower question: **does issuer equity
momentum predict bond repricing within comparable credit-risk groups, or is its
conditional alpha explained by risk exposure and stale observations?**

A follow-on experiment requires:

1. A public or licensed bond-month return panel with reliable issuer links, signal availability dates, accrued interest, and cash flows.
2. Lagged bond spread/momentum and issuer equity characteristics, preserving publication lags and missingness.
3. The same eligible universe for bond-only and bond-plus-equity comparisons, across issuers within comparable risk groups.
4. Measured holdings, issuer concentration, duration and rating exposures, turnover, borrowing requirements, and execution-delay sensitivity.
5. A genuinely later evaluation period, with selection rules fixed before its returns are inspected.

Distinguish information transmission from stale-price measurement with fresh-price
subsets and executable entry-delay tests. Merely shifting published factor returns
does not simulate execution. An issuer signal is constant within issuer-month, so
issuer-by-month fixed effects would absorb it. A within-issuer relative-value question
would require bond-specific characteristics instead.

The [next-experiment design](../research/RESEARCH_AGENDA.md)
specify the counterfactuals, timing, economic endpoints and missing data. This follow-up
is designed, not run. No ratings, holdings or issuer identifiers are inferred from
aggregate factor returns.

## What this project demonstrates

The research contribution is visible in the sequence from hypothesis to conclusion:

- Independent reproduction of a large published-data comparison.
- Explicit handling of factor direction and mixed data provenance.
- A transparent fixed experiment, followed by a dated exploratory amendment.
- Conditional signal attribution and a benchmark scaled without current-return leakage.
- Paired uncertainty, cost headroom and precision interpreted as a research decision.
- A conclusion that survives adverse results and identifies the evidence needed for a stronger claim.

The project supports a bounded empirical contribution: **a reproducible investigation of how equity information, data choices, and implementation assumptions affect corporate bond factor research.**
