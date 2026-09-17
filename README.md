# Do Equity Signals Add to Corporate Bond Factors?

**Incremental alpha, diversification, and the cost budget for adding issuer information.**

An allocation researcher needs to know whether a new signal contributes beyond existing
exposures, whether its diversification beats simply reducing risk, and whether the
increment can pay for implementation. This project answers those questions using
author-released corporate bond factor returns. It reproduces the source comparison,
retains a fixed six-signal baseline, and adds an explicitly exploratory diagnostic study.

## Research questions and answers

| Question | Test implemented here | Finding |
|---|---|---|
| Does issuer equity information add beyond existing bond exposures? | Regress equity-derived bond returns on the three individual bond factors, MKTB and TERM | Composite alpha is inconclusive; momentum and value have opposing conditional alphas |
| Is the combined portfolio better than simply reducing bond exposure? | Scale a bond-only control using the preceding 60 months; compare paired returns and Sharpe intervals | No clear improvement; combined underperforms that control in the later segment |
| How much extra implementation cost can the improvement support? | Incremental mean and HAC interval in bps, with an illustrative 50-bps materiality threshold | Later mean difference is −13.71 bps/year; interval −51.62 to +24.19 bps |
| Are conclusions sensitive to the supplied return database? | Same dates/signals across DFPS, OSBAP and ICE; paired source differences | Small combined-return differences, with strongly dependent sources |

**A useful negative allocation result can coexist with a useful signal-level lead.**
Equity momentum's DFPS conditional alpha is **3.93% annually** (95% interval
**2.04%–5.81%**), and **2.91%** in the later segment. Equity value's full-sample
conditional alpha is **−2.33%**. The equal-weight equity composite has **0.60%** alpha
(**−0.10% to +1.29%**, p = **0.092**). These are gross regression intercepts conditional
on the specified controls, not realized hedged profits. The added analyses use already
inspected history, and cannot establish a new discovery or executable alpha.

![Conditional alpha by issuer signal](research/figures/incremental_alpha.png)

[Methods and exploratory amendment](research/PROTOCOL.md) · [Detailed evidence](docs/04-evaluation.md) · [Next experiments](research/RESEARCH_AGENDA.md)

## Findings

The original fixed combination does **not** establish reliable incremental alpha.
The table below retains its market-plus-TERM benchmark; the new conditional analysis
above also controls for individual bond factors and answers a different question.

| Strategy | Annual mean | Annual volatility | Sharpe | Market + TERM alpha | Alpha p-value |
|---|---:|---:|---:|---:|---:|
| Bond-only | −0.12% | 3.47% | −0.03 | 0.54% | 0.539 |
| Equity-derived bond factors | 0.37% | 2.18% | 0.17 | 0.68% | 0.182 |
| Combined, 50/50 | 0.13% | 2.53% | 0.05 | 0.61% | 0.343 |

*Computed here: 231 months, September 2002–November 2021; DFPS TRACE-derived returns; annualized arithmetic means and alphas; six-lag Newey–West inference; gross of costs. These are long–short factor returns per unit of long-side notional, not returns on a funded long-only portfolio. Benchmark and signal provenance are explained in [Data](docs/01-data.md).*

Three results determine the interpretation:

- **Replication:** all 4,092 statistics in the authors' 341-factor database-comparison table match to numerical precision.
- **Factor direction:** using the source's oriented returns gives the combined portfolio a Sharpe of **0.66**. Applying the documented economic directions reduces it to **0.05**. The first number is a diagnostic of orientation choices, not an alternative successful strategy.
- **Later evaluation:** February 2016–November 2021 produces a **−0.46%** annual mean for the combined portfolio. The conclusion is similar under the alternative OSBAP and ICE return files.

![Cumulative factor P&L](research/figures/cumulative_pnl.png)

## Research contribution

This project demonstrates the research process through inspectable work:

1. **Reproduce before extending.** Reconcile source statistics, dates, units, factor signs, and data vintages.
2. **Connect equity and credit.** Evaluate issuer information through bond portfolios rather than treating equity-factor returns as bond returns.
3. **Test incremental value.** Separate composite allocation performance from conditional signal alpha, use a control scaled with prior information, and quantify paired uncertainty.
4. **Make a research decision.** Compare the incremental cost budget with a stated materiality threshold, diagnose precision, and specify the evidence needed for a new security-level test.

The maintained workflow is in `research/`, with narrative reports in `docs/` and
an executed `study.ipynb`. Every reported result comes from that workflow. External
researchers receive credit for their source datasets and portfolios.

## Read the study

| Chapter | Research question |
|---|---|
| [1. Data](docs/01-data.md) | What exactly is observed, and what does TRACE provenance establish? |
| [2. Factors and evidence](docs/02-factors.md) | Does issuer information add conditional alpha, and which components explain it? |
| [3. Portfolio construction](docs/03-portfolios.md) | Does adding signals beat reducing bond exposure using prior volatility? |
| [4. Evaluation](docs/04-evaluation.md) | What do uncertainty, cost headroom, and source differences imply? |
| [5. Applications](docs/05-applications.md) | Which mechanism deserves a new security-level test? |

[Combined research notebook](study.ipynb) · [Protocol](research/PROTOCOL.md) · [Source register](research/SOURCES.md) · [Exact result tables](research/results/) · [Calculation script](research/run_study.py)

## Reproduce the research

In WSL/Linux with Python 3.12 and uv:

~~~bash
uv sync --locked
uv run python research/download_sources.py
uv run python -m unittest discover -s research -p 'test_*.py' -v
uv run python research/build_notebook.py
uv run python research/check_artifacts.py
uv run python research/check_publication.py
~~~

The first download needs internet access. Analysis uses cached archives, checks their recorded SHA-256 hashes, and saves tables and figures under research/results/ and research/figures/. The notebook builder reruns the study and executes the combined notebook; the artifact checker independently verifies calculations and saved outputs; the publication checker verifies the proposed file set. A failed download can be restarted; completed archives are reused. Hash mismatches require investigating a changed source release, not silently accepting new data.

The study is a research artifact, with a small environment for regenerating its evidence. It does not require the original private TRACE database. pyproject.toml and uv.lock define the single supported environment.

Raw archives, extracted benchmarks and monthly return panels are generated locally
and excluded from version control. The public repository retains summary statistics,
original figures, source URLs/checksums and the executed notebook. See the
[publication review](PUBLICATION.md) for the file policy, clean-export command,
Git-history limitation and considerations for adapting the study into a blog post.

## Repository layout

- `docs/`: data, factors, portfolios, evaluation and applications.
- `research/`: download, calculation, notebook-build and validation scripts; unit tests.
- `research/results/` and `research/figures/`: inspectable summary evidence.
- `research/data/source_manifest.json`: pinned input URLs and SHA-256 checksums.
- `study.ipynb`: executed report and calculation appendix.

GitHub Actions runs the locked-environment setup, unit tests and publication-file
checks on pushes and pull requests. Full numerical reproduction uses the commands
above and the separately downloaded source archives.

## Interpretation and attribution

The later segment is a chronological diagnostic, **not a pristine out-of-sample discovery test**: signals were known in the literature and historical data had already been revised. The six-signal result does not reject every corporate bond strategy, prove market efficiency, or independently reproduce the authors' underlying transaction cleaning.

Primary sources include [Dick-Nielsen et al., replication framework](https://www.aqr.com/insights/research/working-paper/corporate-bond-factors-replication-failures-and-a-new-framework), [Open Source Bond Asset Pricing data](https://openbondassetpricing.com/machine-learning-data/), and the literature documented in the [source register](research/SOURCES.md). External data retain their own terms; see [data attribution](research/DATA_NOTICE.md).

Research revision: 16 September 2026. Historical data coverage ends in 2021 for the common comparison; this is not a current-market backtest. The new diagnostics are an exploratory amendment, not a retrospectively preregistered experiment.
