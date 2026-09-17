"""Check saved research outputs, report links, and notebook execution evidence."""
import base64
import csv
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import unquote
import zipfile

import nbformat
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "research"


def check_links(text, base):
    for target in re.findall(r"!?\[[^\]]*\]\(([^\s)]+)\)", text):
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        path = (base/unquote(target.split("#")[0])).resolve()
        assert path.exists(), f"Broken local link: {base} -> {target}"


def main():
    files = [*ROOT.glob("*.md"), *ROOT.glob("docs/*.md"), *RESEARCH.glob("*.md")]
    for path in files:
        check_links(path.read_text(), path.parent)
    metadata = json.loads((RESEARCH/"results/study_metadata.json").read_text())
    results = pd.read_csv(RESEARCH/"results/performance.csv")
    # Independently compute the primary combined mean and Sharpe using csv/math,
    # without importing run_study's selection, combination, or performance functions.
    names = ["VW_18_spread", "VW_12_mom6*", "VW_27_volatility", "VW_ret_6_1", "VW_be_me", "VW_gp_at*"]
    directions = [1, -1, -1, 1, 1, -1]
    with zipfile.ZipFile(RESEARCH/"data/raw/ExcessLongShortVW_All_Databases.zip") as z:
        rows = list(csv.DictReader(z.read("ExcessLongShortVW_DFPS.csv").decode().splitlines()))
    y = np.array([sum(float(row[name])*direction for name, direction in zip(names, directions))/6 for row in rows])
    stored = results.query("dataset == 'DFPS' and sample == 'Full' and strategy == 'Combined'").iloc[0]
    np.testing.assert_allclose(stored.annual_mean_pct, sum(y)/len(y)*1200, atol=1e-12)
    np.testing.assert_allclose(stored.sharpe, np.mean(y)/np.std(y, ddof=1)*np.sqrt(12), atol=1e-12)
    b = pd.read_csv(RESEARCH/"results/benchmarks.csv")
    assert b.date.tolist() == [row["date"] for row in rows]
    design = np.column_stack([np.ones(len(y)), b[["MKTB", "TERM"]].to_numpy()])
    coef = np.linalg.lstsq(design, y, rcond=None)[0]
    np.testing.assert_allclose(stored.market_term_alpha_pct, coef[0]*1200, atol=1e-12)

    # Reconstruct amendment inputs from raw columns, not the analysis helpers.
    signals = np.array([[float(row[name])*direction for name, direction in zip(names, directions)]
                        for row in rows])
    bond = signals[:, :3].mean(axis=1)
    equity = signals[:, 3:].mean(axis=1)
    spanning = pd.read_csv(RESEARCH/"results/incremental_spanning.csv")
    design = np.column_stack([np.ones(len(y)), signals[:, :3], b[["MKTB", "TERM"]]])
    targets = {"Equity-derived": equity, "Equity momentum": signals[:, 3],
               "Equity value": signals[:, 4], "Equity profitability": signals[:, 5]}
    for sample, start in [("Full", 0), ("Evaluation", metadata["development_months"])]:
        for target, values in targets.items():
            alpha = np.linalg.lstsq(design[start:], values[start:], rcond=None)[0][0]*1200
            row = spanning.loc[(spanning.dataset == "DFPS") & (spanning["sample"] == sample)
                               & (spanning.target == target) & (spanning.lags == 6)].iloc[0]
            np.testing.assert_allclose(row.annual_alpha_pct, alpha, atol=1e-11)
    controlled = pd.read_csv(RESEARCH/"results/risk_control_returns_dfps.csv")
    weights = np.array([min(1, np.std(y[t-60:t], ddof=1)/np.std(bond[t-60:t], ddof=1))
                        for t in range(60, len(y))])
    np.testing.assert_allclose(controlled.bond_weight, weights, atol=1e-12)
    control_returns = weights*bond[60:]
    np.testing.assert_allclose(controlled["Risk-scaled bond"], control_returns, atol=1e-12)
    assert controlled.date.tolist() == [row["date"] for row in rows[60:]]
    assert controlled.training_end.tolist() == [row["date"] for row in rows[59:-1]]
    budgets = pd.read_csv(RESEARCH/"results/incremental_cost_budget.csv")
    for sample, start in [("Post-warmup", 0), ("Evaluation", metadata["development_months"]-60)]:
        diff = (y[60:]-control_returns)[start:]
        n = len(diff)
        residual = diff-diff.mean()
        meat = residual@residual
        for lag in range(1, 7):
            meat += 2*(1-lag/7)*(residual[lag:]@residual[:-lag])
        se = np.sqrt(meat/n**2*n/(n-1))*120000
        mean = diff.mean()*120000
        row = budgets.loc[(budgets.dataset == "DFPS") & (budgets["sample"] == sample)
                          & (budgets.control == "Risk-scaled bond")].iloc[0]
        np.testing.assert_allclose([row.annual_incremental_mean_bps, row.ci_low_bps, row.ci_high_bps],
                                   [mean, mean-1.96*se, mean+1.96*se], atol=1e-10)
    amendment = json.loads((RESEARCH/"results/incremental_metadata.json").read_text())
    for key, name in [("protocol_sha256", "PROTOCOL.md"), ("code_sha256", "incremental.py")]:
        assert amendment[key] == hashlib.sha256((RESEARCH/name).read_bytes()).hexdigest()

    notebook = nbformat.read(ROOT/"study.ipynb", as_version=4)
    nbformat.validate(notebook)
    code_cells = [cell for cell in notebook.cells if cell.cell_type == "code"]
    assert [c.execution_count for c in code_cells] == list(range(1, len(code_cells)+1))
    png_hashes = set()
    for cell in notebook.cells:
        if cell.cell_type == "markdown":
            check_links(cell.source, ROOT)
        else:
            for output in cell.outputs:
                assert output.output_type != "error"
                if "image/png" in output.get("data", {}):
                    png_hashes.add(hashlib.sha256(base64.b64decode(output.data["image/png"])).hexdigest())
    for figure in (RESEARCH/"figures").glob("*.png"):
        assert hashlib.sha256(figure.read_bytes()).hexdigest() in png_hashes
    assert metadata["replication"]["nonmissing_comparisons"] == 4092
    print(f"Verified {len(files)} Markdown files, all notebook links, {len(code_cells)} executed code cells, and {len(png_hashes)} embedded figures.")
    print("Primary mean, Sharpe, alpha, conditional alphas, lagged weights and incremental cost intervals independently agree with the raw archive.")
    print("Author-table replication covers 4,092 values; amendment code/protocol hashes match.")


if __name__ == "__main__":
    main()
