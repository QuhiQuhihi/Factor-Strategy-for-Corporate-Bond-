"""Refresh the combined research report and execute its calculation appendix."""
from __future__ import annotations

import json
import os
from pathlib import Path
import re
from urllib.parse import quote, unquote

import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ["(Chapter1)Data", "(Chapter2)Factor_model", "(Chapter3)Porfrolio_model",
           "(Chapter4)Evaluation", "(Chapter5)Application"]


def rebase_links(text: str, directory: Path) -> str:
    def convert(match):
        target = match.group(2)
        if target.startswith(("https://", "http://", "#", "mailto:")):
            return match.group(0)
        path, separator, fragment = target.partition("#")
        resolved = (directory / unquote(path)).resolve().relative_to(ROOT)
        new = quote(resolved.as_posix(), safe="/") + (separator + fragment if separator else "")
        return match.group(1) + new + match.group(3)
    text = re.sub(r"(!?\[[^\]]*\]\()([^\s)]+)(\))", convert, text)
    return re.sub(r"~~~math\n(.*?)\n~~~", lambda m: "$$\n"+m.group(1)+"\n$$", text, flags=re.S)


def main():
    os.environ.setdefault("JUPYTER_RUNTIME_DIR", "/tmp/corporate-bond-jupyter")
    os.environ.setdefault("IPYTHONDIR", "/tmp/corporate-bond-ipython")
    os.environ.setdefault("MPLCONFIGDIR", "/tmp/corporate-bond-matplotlib")
    md = nbformat.v4.new_markdown_cell
    code = nbformat.v4.new_code_cell
    cells = [md("""# Do Equity Signals Add to Corporate Bond Factors?

## Summary

The fixed six-signal combination has no clear advantage over reducing bond exposure.
An exploratory conditional regression reveals opposing issuer-signal effects:
equity momentum alpha is 3.93%, value alpha is −2.33%, and composite alpha is
inconclusive at 0.60% (95% interval −0.10% to +1.29%). These are annualized gross
intercepts, not feasible hedged returns. The later combined-minus-risk-control mean
is −13.71 bps/year, with a −51.62 to +24.19 interval.

The source-table replication matches 4,092 values. The original fixed combination
has a 0.13% annual mean and 0.05 Sharpe over 231 months, September 2002–November 2021.
The lagged risk control uses 60 training months and 171 comparison months.

[Repository overview](README.md) · [Protocol](research/PROTOCOL.md) · [Sources](research/SOURCES.md)

## Context and methods

This is an individual research replication and extension using public author-released
bond factor returns. The chapters distinguish attributed literature findings from
new calculations. The calculation appendix reruns the study from the cached source archives.

### Key assumptions

Six fixed economic directions; no performance-selected weights; gross long–short
returns per fixed long-side notional; common monthly observations; six-lag HAC inference.
Historical revisions and literature selection limit out-of-sample interpretation.
The 16 September 2026 amendment was designed after inspecting the original results.
It adds conditional controls, a lagged risk benchmark, paired uncertainty and cost
headroom. Its statistical families do not correct for all prior research choices.
""")]
    for name in REPORTS:
        report = (ROOT/name/"README.md").read_text()
        report = rebase_links(report, ROOT/name)
        report = re.sub(r"^# ", "## ", report, count=1)
        cells.append(md(report))
    cells.extend([
        md("""## Executed research appendix

### 1. Recompute the evidence

Run `uv sync --locked` and `uv run python research/download_sources.py` first.
The following cell checks source hashes and regenerates all tables and figures.
It performs no network request and does not execute the legacy scripts."""),
        code("""from pathlib import Path
import contextlib
import io
import json
import sys
import pandas as pd
from IPython.display import display, Image

root = Path.cwd()
if not (root / 'research/run_study.py').exists():
    raise RuntimeError('Run this notebook from the repository root')
sys.path.insert(0, str(root / 'research'))
from run_study import main, COMPOSITES
with contextlib.redirect_stdout(io.StringIO()):
    main()
metadata = json.loads((root / 'research/results/study_metadata.json').read_text())
display(pd.Series({k: metadata[k] for k in ['sample_start', 'sample_end', 'months', 'evaluation_start']}))
display(pd.Series(metadata['replication']))"""),
        md("### 2. Inspect primary and later-period performance\n\nMeans and alphas below are annualized percentages; Sharpe is unitless."),
        code("""performance = pd.read_csv(root / 'research/results/performance.csv')
view = performance.loc[
    (performance.dataset == 'DFPS') & performance.strategy.isin(COMPOSITES)
    & performance['sample'].isin(['Full', 'Evaluation']),
    ['sample', 'strategy', 'n', 'annual_mean_pct', 'annual_vol_pct', 'sharpe',
     'market_term_alpha_pct', 'market_term_alpha_p', 'market_term_alpha_q']]
display(view.round(3).reset_index(drop=True))"""),
        md("### 3. Examine the path and uncertainty\n\nCumulative P&L uses fixed notional, not compounded fund wealth. Intervals are pointwise HAC intervals."),
        code("display(Image(filename=str(root / 'research/figures/cumulative_pnl.png')))"),
        code("display(Image(filename=str(root / 'research/figures/alpha_intervals.png')))"),
        md("### 4. Check exposure relationships and orientation"),
        code("display(Image(filename=str(root / 'research/figures/signal_correlations.png')))"),
        code("""orientation = pd.read_csv(root / 'research/results/orientation_sensitivity.csv')
display(orientation.loc[orientation.strategy.isin(COMPOSITES)].round(3).reset_index(drop=True))"""),
        md("""### 5. Incremental issuer information

The new model controls for the three bond factors as well as MKTB and TERM. Intervals
are pointwise; four-test BH families include the composite and its three components.
This is conditional alpha attribution, not a full mean-variance spanning test."""),
        code("""conditional = pd.read_csv(root / 'research/results/incremental_spanning.csv')
view = conditional.loc[(conditional.dataset == 'DFPS') & (conditional.lags == 6)
    & conditional['sample'].isin(['Full', 'Evaluation']),
    ['sample', 'target', 'annual_alpha_pct', 'alpha_ci_low_pct', 'alpha_ci_high_pct', 'alpha_q']]
display(view.rename(columns={'annual_alpha_pct': 'Alpha %/year', 'alpha_ci_low_pct': '95% low',
    'alpha_ci_high_pct': '95% high', 'alpha_q': 'BH q'}).round(4).reset_index(drop=True))"""),
        code("display(Image(filename=str(root / 'research/figures/incremental_alpha.png')))"),
        md("""Momentum and value have opposing conditional alphas. The composite remains
inconclusive. Both the regression controls and the testing family differ from the
original market/TERM-only analysis; a selected regression result is not a live strategy.

### 6. Compare with reducing bond exposure

The control scales bond-only exposure using the preceding 60 months. Unused reference
notional earns zero excess P&L. The realized risks need not match exactly."""),
        code("""controls = pd.read_csv(root / 'research/results/risk_control_performance.csv')
display(controls.loc[controls.dataset == 'DFPS',
    ['sample', 'n', 'strategy', 'annual_mean_pct', 'annual_vol_pct', 'sharpe']]
    .rename(columns={'annual_mean_pct': 'Mean %/year', 'annual_vol_pct': 'Vol %/year'})
    .round(3).reset_index(drop=True))"""),
        md("""### 7. Cost headroom and paired uncertainty

Cost headroom is the mean difference versus the risk-scaled bond control, not an
estimate of transaction costs. The 50-bps threshold is an illustrative materiality
convention; the detectable effect is a normal/HAC precision approximation."""),
        code("""budget = pd.read_csv(root / 'research/results/incremental_cost_budget.csv')
display(budget.loc[(budget.dataset == 'DFPS') & (budget.control == 'Risk-scaled bond'),
    ['sample', 'annual_incremental_mean_bps', 'ci_low_bps', 'ci_high_bps', 'approximate_mde_80pct_bps']]
    .rename(columns={'annual_incremental_mean_bps': 'Mean bps/year', 'ci_low_bps': '95% low',
    'ci_high_bps': '95% high', 'approximate_mde_80pct_bps': '80% MDE bps/year'})
    .round(2).reset_index(drop=True))"""),
        md("Paired circular-block percentile intervals below are descriptive, conditional on realized paths and weights, and do not correct for selection."),
        code("""intervals = pd.read_csv(root / 'research/results/sharpe_difference_intervals.csv')
display(intervals.loc[(intervals.dataset == 'DFPS') & (intervals.control == 'Risk-scaled bond'),
    ['sample', 'block_months', 'sharpe_difference', 'ci_low', 'ci_high']]
    .rename(columns={'block_months': 'Block months', 'sharpe_difference': 'Sharpe difference',
                     'ci_low': '95% low', 'ci_high': '95% high'})
    .round(3).reset_index(drop=True))"""),
        md("### 8. Paired source sensitivity\n\nSame dates and signals; source agreement is dependent evidence."),
        code("""source_pairs = pd.read_csv(root / 'research/results/paired_source_differences.csv')
display(source_pairs.loc[source_pairs['sample'] == 'Full',
    ['source_a', 'source_b', 'annual_mean_a_minus_b_bps', 'ci_low_bps', 'ci_high_bps', 'monthly_correlation']]
    .rename(columns={'annual_mean_a_minus_b_bps': 'A minus B bps/year', 'ci_low_bps': '95% low',
                     'ci_high_bps': '95% high', 'monthly_correlation': 'Correlation'})
    .round(3).reset_index(drop=True))"""),
        md("""## Takeaways

The archived source comparison reproduces exactly, but the chosen economic-direction
portfolio offers weak gross performance. Lower volatility is observable; reliable
incremental allocation benefit is not. The source-oriented version has different
exposures and cannot be substituted as evidence that the economic-direction hypothesis succeeded.

All three return sources produce a negative combined mean in the later period. The
factor-level diagnostics are complete. Positive conditional momentum alpha and
negative value alpha motivate a narrower question: issuer information transmission
versus common risk and stale prices. That follow-up requires matched security holdings,
point-in-time information, execution observations and an uninspected later sample.

No transaction-level TRACE cleaning, security-level integration, or estimated net-cost
backtest is claimed. Detailed provenance and scope are in [SOURCES.md](research/SOURCES.md).
""")
    ])
    for i, cell in enumerate(cells):
        cell.id = f"research-{i:02d}"
    notebook = nbformat.v4.new_notebook(cells=cells, metadata={
        "kernelspec": {"display_name": "Python 3 (research)", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.12"}})
    nbformat.validate(notebook)
    NotebookClient(notebook, timeout=180, kernel_name="python3", resources={"metadata": {"path": str(ROOT)}}).execute()
    nbformat.validate(notebook)
    if any(output.output_type == "error" for cell in notebook.cells if cell.cell_type == "code" for output in cell.outputs):
        raise RuntimeError("Notebook contains errors")
    destination = ROOT / "Combined_README.ipynb"
    nbformat.write(notebook, destination)
    print(f"Saved executed report: {destination.name} ({len(cells)} cells)")


if __name__ == "__main__":
    main()
