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
    os.environ.setdefault("MPLCONFIGDIR", "/tmp/corporate-bond-matplotlib")
    md = nbformat.v4.new_markdown_cell
    code = nbformat.v4.new_code_cell
    cells = [md("""# Corporate Bond Factors: Replication and Equity Signals

## Summary

The fixed six-signal combination does not establish reliable incremental alpha.
This notebook contains the updated chapter reports and an executed research appendix.
The primary comparison uses 231 months, September 2002–November 2021. The source-table
replication matches 4,092 values; the new combination has a 0.13% annual mean and 0.05
Sharpe, with a negative later evaluation segment.

[Repository overview](README.md) · [Protocol](research/PROTOCOL.md) · [Sources](research/SOURCES.md)

## Context and methods

This is an individual research replication and extension using public author-released
bond factor returns. The chapters distinguish attributed literature findings from
new calculations. The calculation appendix reruns the study from the cached source archives.

### Key assumptions

Six fixed economic directions; no performance-selected weights; gross long–short
returns per fixed long-side notional; common monthly observations; six-lag HAC inference.
Historical revisions and literature selection limit out-of-sample interpretation.
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
        md("""## Takeaways

The archived source comparison reproduces exactly, but the chosen economic-direction
portfolio offers weak gross performance. Lower volatility is observable; reliable
incremental alpha is not. The source-oriented version has different exposures and cannot
be substituted as evidence that the prespecified hypothesis succeeded.

All three return sources produce a negative combined mean in the later period. The
factor-level result is complete; matched security holdings, execution delays, issuer
constraints and trading costs require a separate empirical study.

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
