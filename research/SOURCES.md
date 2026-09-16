# Sources and evidence register

Reviewed 15 September 2026. The research reports distinguish **reported literature
findings**, **reproduced source statistics**, and **new calculations**. Source downloads
are versioned by [URL and SHA-256](data/source_manifest.json).

## Numerical inputs

| Source and version | Exact object | Treatment here |
|---|---|---|
| [Open Source Bond Asset Pricing, July 2025 archive](https://openbondassetpricing.com/wp-content/uploads/2025/07/ExcessLongShortVW_All_Databases.zip) | ExcessLongShortVW_DFPS.csv, ExcessLongShortVW_OSBAP.csv, ExcessLongShortVW_ICE.csv; 341 signals each | Primary DFPS result and two alternative-source checks; original source labels retained |
| Same archive | DatabaseComparison_DNR_2022.csv and database_comparison.py | Reproduce all 341 × 12 table cells; author's monthly percentage means, annualized Sharpe ratios, correlations and paired iid t-tests; stored signs retained for replication |
| [November 2024 factor archive](https://openbondassetpricing.com/wp-content/uploads/2024/11/Factor_Time_Series_LongShort.zip) | DurAdjLongShortVW.csv | ICE duration-adjusted sensitivity; restore signs using this file's own starred columns |
| Same archive | ExcessLongShortVW.csv, TurnOverLongShortVW.csv | Inventory only; no claim that source turnover identifies netted TRACE strategy turnover |
| [Co-pricing archive, December 2025](https://openbondassetpricing.com/wp-content/uploads/2025/12/djm_data.zip) | traded_bond_excess.csv: MKTB and TERM | Decimal monthly benchmark returns; DD/MM/YYYY parsed explicitly; neither a DFPS-universe index nor a security-specific hedge |

The source-comparison replication preserves the authors' sample restrictions: DFPS
ends in November 2021; OSBAP is truncated at that end date; ICE is restricted to the
DFPS start and end. Comparisons handle missing observations pairwise. The six-signal
extension instead uses the balanced common sample, as specified in [PROTOCOL.md](PROTOCOL.md).

## Literature: what each source establishes

### Dickerson, Mueller and Robotti — Priced Risk in Corporate Bonds

- Version: 2023 working-paper copy; published in *Journal of Financial Economics* 150,
  article 103707. [Paper](https://wrap.warwick.ac.uk/id/eprint/178961/1/WRAP-Priced-risk-corporate-bonds-23.pdf)
- Evidence location: §2.1, July 2002–December 2016 Enhanced TRACE/FISD inputs; Tables 1–2
  and the model-comparison discussion. Some estimation samples are shorter because
  characteristics require history.
- Reported finding: little incremental pricing evidence for the examined factors over
  the corporate bond market, with liquidity a marginal exception.
- Use here: motivate the market benchmark and temporal-alignment checks. Its numerical
  factor tables are **not** claimed as reproduced by the differently sampled 341-factor exercise.

### Dick-Nielsen, Feldhütter, Pedersen and Stolborg — Corporate Bond Factors: Replication Failures and a New Framework

- Version: [AQR research summary, 5 October 2023](https://www.aqr.com/insights/research/working-paper/corporate-bond-factors-replication-failures-and-a-new-framework).
- Evidence location: summary paragraphs on replication, representative firm bonds, and
  equity signals. The linked paper has subsequent revisions; this study does not assign
  a table number or numerical estimate based only on the summary.
- Reported finding: several factors fail replication, while some bond and issuer equity
  signals survive under the authors' framework.
- Use here: economic motivation; the distributed DFPS return file supplies an empirical
  input through the July 2025 comparison archive. [Authors' processing repository](https://github.com/Cstolborg/corp-bond-data)
  describes the TRACE/FISD/CRSP inputs and required WRDS access; its processing is not rerun here.

### Dickerson, Nozawa and Robotti — Factor Investing with Delays

- Versions: [October 2024 paper](https://www.cesarerobotti.com/wp-content/uploads/2024/10/DNR_Bond_Anomalies.pdf)
  and [July 2025 discussion paper](https://www.ier.hit-u.ac.jp/Common/publication/DP/DPS-A771.pdf).
- Evidence location: 2025 §5.1 and footnote 26, Table A.1, and Table A.6. The numerical
  archive used here contains August 2002–November 2022 ICE observations; the common
  DFPS comparison ends earlier.
- Reported finding: trading delays can materially erode gross factor performance.
  The study's gross-positive orientation is explicitly retrospective.
- Use here: characteristic definitions, monthly decile/value-weighting convention,
  and the distinction between gross performance and executable returns. Published delay
  costs are **not** inserted into this study's portfolios or described as our estimates.

### Dickerson, Robotti and Rossetti — The Corporate Bond Factor Replication Crisis

- Version: [April 2026 working paper](https://openbondassetpricing.com/wp-content/uploads/2026/04/corp-bond-replication-crisis-dickerson.pdf).
- Evidence location: introduction, §§3–5, and factor tables, with many series covering
  September 2002–December 2024.
- Reported finding: only 26 of 432 examined alpha specifications survive the reported
  BH adjustment; measurement error and future-dependent return filtering can affect
  inference materially.
- Use here: motivate construction checks and disclose that the July 2025 six-signal archive
  is **not** a replication of the newer 108-signal, bias-corrected exercise.

### Dickerson, Julliard and Mueller — The Co-Pricing Factor Zoo

- Version: [April 2026 arXiv v1](https://arxiv.org/html/2604.04430v1), using the separately
  dated December 2025 data bundle. Earlier drafts circulated as *The Corporate Bond Factor Zoo*.
- Evidence location: Appendix A, Table A.1, defines MKTB and TERM. The archive spans
  January 1986–December 2022.
- Reported finding: a broad joint bond/equity pricing model can aggregate information
  across many factors; its target and model class differ from a fixed six-signal portfolio.
- Use here: benchmark definitions only. The reported Bayesian model, SDF, and investment
  performance are not estimated or claimed in this project.

### Jensen, Kelly and Pedersen — Global Factor Data

- [Documentation](https://jkpfactors-data.s3.amazonaws.com/documents/Documentation.pdf),
  inspected September 2026: characteristic definitions and original literature signs.
- Evidence location: momentum formula for ret_6_1; characteristics table entries for
  book-to-market equity (be_me) and gross profits-to-assets (gp_at).
- Use here: map issuer equity signals to meaningful economic concepts. The data are used
  through the bond factor release; no stock return portfolios are substituted for bond returns.

## Why the sources can disagree

The studies differ in periods, return providers, cleaning, execution assumptions, signal
definitions, portfolio sorts, benchmarks, and the model being tested. A weak factor-series
combination does not refute a broad cross-sectional pricing model. Reproducing an author
summary table does not certify the underlying trade records. The reports preserve these
distinctions rather than treating one paper as universal evidence for or against credit factors.

## Boundaries and source availability

The [provider's machine-learning page](https://openbondassetpricing.com/machine-learning-data/)
documents ICE/BAML predictor origins and starred return columns. Its
[public-panel page](https://openbondassetpricing.com/data/) explains omitted proprietary
fields. No matched security panel is used in the current study. Thus there is no new
issuer-balanced backtest, exact trading-cost estimate, or investment-grade-only inference.

The source site is actively revised. The cached archive hashes identify what was actually
analyzed; a changed live file is not automatically equivalent. Link availability, paper
publication status, and subsequent source revisions do not change the saved experiment.
