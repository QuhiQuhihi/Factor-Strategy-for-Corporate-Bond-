# 5. Applications: what the evidence supports

[Evaluation](../%28Chapter4%29Evaluation/README.md) · [Overview](../README.md)

## Research conclusion

Equity-derived bond signals can change portfolio exposures and reduce volatility in the tested combination. They do not deliver statistically reliable incremental alpha here, and the later evaluation segment is negative before trading costs.

The useful output is a documented method for deciding whether an apparent credit factor deserves further investigation. It can support research prioritization and risk analysis; it does not yet justify deploying this portfolio.

## Practical uses

### Factor due diligence

Start by reproducing a provider's own statistics. Then inspect its sign conventions, information dates, weighting, return definition, and universe. This project reproduces the source table exactly, yet obtains a much lower combined Sharpe after applying the originally hypothesized directions.

That distinction matters when evaluating a proposed signal: a reproducible historical premium can still depend on an economically different trade or an infeasible construction.

### Credit exposure analysis

Credit spreads and low volatility largely offset in the tested portfolios. Equal signal weights therefore offer an incomplete picture of risk. A portfolio researcher can use the factor correlation matrix and market/TERM regressions as diagnostics before imposing bond-level duration, spread, rating, and issuer constraints.

The regression alpha is conditional on the selected benchmark. It is not a valuation estimate for an individual illiquid bond.

### Equity information in bond research

Issuer equity momentum, valuation, and profitability remain plausible inputs to a broader credit research process. Here, equity momentum's full-sample market-plus-TERM alpha has a nominal p-value of 0.049, but q = 0.244 after the stated multiple-testing adjustment. This is a reason to investigate its mechanism and stability, not a confirmed signal.

Future work should distinguish information about improving issuer fundamentals from compensation for changing credit risk. Bond and equity claims occupy different positions in the capital structure, so an equity-style label alone does not determine the appropriate credit trade.

## A focused next experiment

The completed factor-series study leaves one useful security-level question: **does a joint issuer-equity and bond-characteristic score improve selection within comparable credit-risk groups?**

A follow-on experiment would require:

1. A public or licensed bond-month return panel with reliable issuer links, signal availability dates, accrued interest, and cash flows.
2. Lagged bond spread/momentum and issuer equity characteristics, preserving publication lags and missingness.
3. The same eligible universe for separate-sleeve and integrated-score portfolios.
4. Measured holdings, issuer concentration, duration and rating exposures, turnover, borrowing requirements, and execution-delay sensitivity.
5. A genuinely later evaluation period, with selection rules fixed before its returns are inspected.

Ratings and issuer identifiers cannot be inferred from aggregate factor returns. The current public-data study therefore completes the replication and factor-combination question without claiming that this next experiment has been performed.

## What this project demonstrates

The research contribution is visible in the sequence from hypothesis to conclusion:

- Independent reproduction of a large published-data comparison.
- Explicit handling of factor direction and mixed data provenance.
- A transparent, fixed bond-plus-equity experiment.
- Statistical inference that distinguishes a positive point estimate from supported alpha.
- A conclusion that survives adverse results and identifies the evidence needed for a stronger claim.

The original ambition to build an “optimal corporate bond strategy” is too strong for the available evidence. The updated project supports a narrower, defensible claim: **a reproducible investigation of how equity information, data choices, and implementation assumptions affect corporate bond factor research.**
