"""Run replication, fixed portfolios and exploratory diagnostics from cached archives."""
from __future__ import annotations

import hashlib
import json
import math
import os
from pathlib import Path
import zipfile

os.environ.setdefault("MPLCONFIGDIR", "/tmp/corporate-bond-matplotlib")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm
from statsmodels.stats.multitest import multipletests

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "data" / "raw"
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
ARCHIVE = "ExcessLongShortVW_All_Databases.zip"
# Economic direction applies to high-characteristic minus low-characteristic returns.
SIGNALS = {
    "Credit spread": ("VW_18_spread", 1, "Bond"),
    "Bond momentum": ("VW_12_mom6", 1, "Bond"),
    "Low volatility": ("VW_27_volatility", -1, "Bond"),
    "Equity momentum": ("VW_ret_6_1", 1, "Equity-derived"),
    "Equity value": ("VW_be_me", 1, "Equity-derived"),
    "Equity profitability": ("VW_gp_at", 1, "Equity-derived"),
}
COMPOSITES = ["Bond-only", "Equity-derived", "Combined"]
COLORS = {"Bond-only": "#b54e38", "Equity-derived": "#157f79", "Combined": "#234a80"}


def read_member(archive: str, member: str, dayfirst: bool = False) -> pd.DataFrame:
    with zipfile.ZipFile(RAW / archive) as z:
        df = pd.read_csv(z.open(member))
    df["date"] = pd.to_datetime(df["date"], dayfirst=dayfirst)
    df = df.set_index("date").sort_index()
    if df.index.has_duplicates or df.index.to_period("M").has_duplicates:
        raise ValueError(f"Duplicate months in {member}")
    if not df.index.equals(df.index + pd.offsets.MonthEnd(0)):
        raise ValueError(f"Dates are not month ends: {member}")
    if not np.isfinite(df.to_numpy()[~df.isna().to_numpy()]).all():
        raise ValueError(f"Nonfinite values in {member}")
    return df


def select_signals(df: pd.DataFrame) -> tuple[pd.DataFrame, list[dict]]:
    result = pd.DataFrame(index=df.index)
    mapping = []
    for label, (base, direction, family) in SIGNALS.items():
        matches = [c for c in df if c.rstrip("*") == base]
        if len(matches) != 1:
            raise ValueError(f"Expected exactly one column for {base}: {matches}")
        col = matches[0]
        source_sign = -1 if col.endswith("*") else 1
        multiplier = source_sign * direction
        result[label] = df[col] * multiplier
        mapping.append(dict(signal=label, source_column=col, family=family,
                            source_sign=source_sign, economic_direction=direction,
                            applied_multiplier=multiplier))
    return result, mapping


def combine(signals: pd.DataFrame) -> pd.DataFrame:
    if signals.isna().any().any():
        raise ValueError("Do not silently change portfolio weights around missing factors")
    out = signals.copy()
    out["Bond-only"] = signals[list(SIGNALS)[:3]].mean(axis=1)
    out["Equity-derived"] = signals[list(SIGNALS)[3:]].mean(axis=1)
    out["Combined"] = (out["Bond-only"] + out["Equity-derived"]) / 2
    out["Combined minus bond"] = out["Combined"] - out["Bond-only"]
    return out


def fit_hac(y: pd.Series, x: pd.DataFrame | None = None, lags: int = 6):
    design = np.ones((len(y), 1)) if x is None else sm.add_constant(x).to_numpy()
    if len(y) <= design.shape[1] + lags or np.linalg.matrix_rank(design) != design.shape[1]:
        raise ValueError("Insufficient observations or rank-deficient regression")
    return sm.OLS(y.to_numpy(), design).fit(cov_type="HAC", cov_kwds={"maxlags": lags, "use_correction": True}, use_t=False)


def performance(df: pd.DataFrame, benchmark: pd.DataFrame, sample: str, dataset: str) -> pd.DataFrame:
    rows = []
    for name, y in df.items():
        fit = fit_hac(y)
        # Fixed-notional cumulative P&L, with zero inception P&L included in the peak.
        pnl = y.cumsum()
        peaks = pnl.cummax().clip(lower=0)
        row = dict(dataset=dataset, sample=sample, strategy=name, n=len(y),
                   start=y.index.min().strftime("%Y-%m"), end=y.index.max().strftime("%Y-%m"),
                   annual_mean_pct=1200*y.mean(), annual_vol_pct=100*np.sqrt(12)*y.std(ddof=1),
                   sharpe=np.sqrt(12)*y.mean()/y.std(ddof=1),
                   mean_t=fit.tvalues[0], mean_p=fit.pvalues[0],
                   mean_ci_low_pct=1200*(fit.params[0]-1.96*fit.bse[0]),
                   mean_ci_high_pct=1200*(fit.params[0]+1.96*fit.bse[0]),
                   max_pnl_drawdown_pct=100*(pnl-peaks).min(), worst_month_pct=100*y.min())
        for model, cols in [("market", ["MKTB"]), ("market_term", ["MKTB", "TERM"])]:
            reg = fit_hac(y, benchmark.loc[y.index, cols])
            row.update({f"{model}_alpha_pct": 1200*reg.params[0],
                        f"{model}_alpha_t": reg.tvalues[0], f"{model}_alpha_p": reg.pvalues[0],
                        f"{model}_alpha_ci_low_pct": 1200*(reg.params[0]-1.96*reg.bse[0]),
                        f"{model}_alpha_ci_high_pct": 1200*(reg.params[0]+1.96*reg.bse[0]),
                        f"{model}_beta": reg.params[1], f"{model}_r2": reg.rsquared})
            if len(cols) == 2:
                row["term_beta"] = reg.params[2]
        rows.append(row)
    out = pd.DataFrame(rows)
    # A family includes six signals, three composites and the pre-specified contrast.
    for p in ["mean_p", "market_alpha_p", "market_term_alpha_p"]:
        out[p.replace("_p", "_q")] = multipletests(out[p], method="fdr_bh")[1]
    return out


def reproduce_author_comparison(raw: dict[str, pd.DataFrame]) -> tuple[pd.DataFrame, dict]:
    # Reproduce the archived author's exact conventions, including sample sign flips
    # and paired iid t-tests. This is separate from the economic-direction HAC study.
    dfs = {k: v.rename(columns=lambda c: c.replace("*", "")) for k, v in raw.items()}
    end = dfs["DFPS"].index.max()
    start = dfs["DFPS"].index.min()
    dfs["OSBAP"] = dfs["OSBAP"].loc[:end]
    dfs["ICE"] = dfs["ICE"].loc[start:end]
    table = pd.DataFrame(index=dfs["DFPS"].columns)
    for a, b in [("DFPS", "OSBAP"), ("DFPS", "ICE"), ("OSBAP", "ICE")]:
        table[f"{a}_{b}"] = dfs[a].corrwith(dfs[b])
        pvals = []
        for col in table.index:
            pair = pd.concat([dfs[a][col], dfs[b][col]], axis=1).dropna()
            pvals.append(stats.ttest_rel(pair.iloc[:, 0], pair.iloc[:, 1]).pvalue)
        table[f"p_value_{a}_{b}"] = pvals
    for k, df in dfs.items():
        table[f"Mean_{k}"] = 100*df.mean()
        table[f"SR_{k}"] = np.sqrt(12)*df.mean()/df.std(ddof=1)
    with zipfile.ZipFile(RAW / ARCHIVE) as z:
        reference = pd.read_csv(z.open("DatabaseComparison_DNR_2022.csv"), index_col=0)
    table = table.loc[reference.index, reference.columns]
    error = (table-reference).abs()
    np.testing.assert_allclose(table, reference, atol=1e-10, rtol=1e-9, equal_nan=True)
    check = {"source": "DatabaseComparison_DNR_2022.csv", "factors": len(table),
             "statistics_per_factor": len(table.columns), "max_absolute_error": float(error.max().max()),
             "nonmissing_comparisons": int(error.notna().sum().sum())}
    detail = []
    for label, (base, _, _) in SIGNALS.items():
        for col in table:
            detail.append(dict(signal=label, statistic=col, reported=reference.loc[base, col],
                               reproduced=table.loc[base, col], absolute_error=error.loc[base, col]))
    pd.DataFrame(detail).to_csv(RESULTS / "replication_selected.csv", index=False)
    table.to_csv(RESULTS / "replication_all_factors.csv", index_label="factor")
    return table, check


def figures(primary: pd.DataFrame, summary: pd.DataFrame):
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11,
                         "axes.spines.top": False, "axes.spines.right": False,
                         "axes.titleweight": "bold", "figure.dpi": 140})
    end = primary.index[-1].strftime("%b %Y")
    start = primary.index[0].strftime("%b %Y")
    split = primary.index[math.floor(len(primary)*.7)]
    fig, ax = plt.subplots(figsize=(10, 5.1), layout="constrained")
    for name, style in zip(COMPOSITES, ["--", "-.", "-"]):
        ax.plot(primary.index, primary[name].cumsum()*100, label=name, color=COLORS[name], linestyle=style, lw=2)
    ax.axhline(0, color="#888888", lw=.7)
    ax.axvline(split, color="#888888", linestyle=":", lw=1)
    ax.set(title="Equity signals change the bond strategy's return path",
           ylabel="Cumulative P&L (% of fixed long-side notional)", xlabel=f"DFPS TRACE returns | {start}–{end} | gross of costs")
    ax.legend(loc="upper left", frameon=False)
    ax.grid(axis="y", alpha=.2)
    ax.text(.99, .02, "Dotted line: final 30% evaluation segment", transform=ax.transAxes, ha="right", fontsize=9)
    fig.savefig(FIGURES / "cumulative_pnl.png")
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.8), layout="constrained", sharex=True)
    for ax, sample in zip(axes, ["Full", "Evaluation"]):
        part = summary.query("dataset == 'DFPS' and sample == @sample").set_index("strategy").loc[COMPOSITES]
        for i, (name, row) in enumerate(part.iterrows()):
            alpha = row.market_term_alpha_pct
            ax.errorbar(alpha, i, xerr=[[alpha-row.market_term_alpha_ci_low_pct],
                                      [row.market_term_alpha_ci_high_pct-alpha]],
                        fmt="o", color=COLORS[name], capsize=5, markersize=7)
        ax.set(yticks=range(3), yticklabels=COMPOSITES, title=f"{sample} sample", xlabel="Annualized alpha (%), market + TERM")
        ax.axvline(0, color="#888888", lw=1)
        ax.set_ylim(2.6, -.6)
        ax.grid(axis="x", alpha=.2)
    fig.suptitle("Positive point estimates do not settle the alpha question\n95% pointwise intervals; Newey–West, six lags", fontsize=13)
    fig.savefig(FIGURES / "alpha_intervals.png")
    plt.close(fig)

    matrix = primary[list(SIGNALS)].corr()
    fig, ax = plt.subplots(figsize=(8.4, 6), layout="constrained")
    im = ax.imshow(matrix, cmap="RdBu_r", vmin=-1, vmax=1)
    labels = ["Credit\nspread", "Bond\nmomentum", "Low\nvolatility", "Equity\nmomentum", "Equity\nvalue", "Equity\nprofitability"]
    ax.set(xticks=range(6), xticklabels=labels, yticks=range(6), yticklabels=list(SIGNALS),
           title="Diversification depends on the direction of each signal")
    for i in range(6):
        for j in range(6):
            v = matrix.iloc[i, j]
            ax.text(j, i, f"{v:.2f}", ha="center", va="center", color="white" if abs(v)>.6 else "#222222")
    fig.colorbar(im, ax=ax, shrink=.8, label="Monthly Pearson correlation")
    fig.savefig(FIGURES / "signal_correlations.png")
    plt.close(fig)

    # The amendment asks about alpha conditional on individual bond factors too.
    conditional = pd.read_csv(RESULTS / "incremental_spanning.csv")
    targets = ["Equity-derived", "Equity momentum", "Equity value", "Equity profitability"]
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.8), layout="constrained", sharex=True)
    for ax, sample in zip(axes, ["Full", "Evaluation"]):
        part = conditional.query("dataset == 'DFPS' and sample == @sample and lags == 6").set_index("target").loc[targets]
        for i, (target, row) in enumerate(part.iterrows()):
            alpha = row.annual_alpha_pct
            ax.errorbar(alpha, i, xerr=[[alpha-row.alpha_ci_low_pct], [row.alpha_ci_high_pct-alpha]],
                        fmt="o" if i == 0 else "s", color="#234a80" if i == 0 else "#157f79",
                        capsize=5, markersize=7)
        ax.set(yticks=range(4), yticklabels=targets, title=f"{sample} sample (n={int(part.n.iloc[0])})",
               xlabel="Annual conditional alpha (%)", ylim=(3.6, -.6))
        ax.axvline(0, color="#888888", lw=1)
        ax.grid(axis="x", alpha=.2)
    fig.suptitle("Issuer equity signals have different conditional alphas\n"
                 "Controls: three bond factors + MKTB + TERM | exploratory, gross of costs", fontsize=12)
    fig.supxlabel("DFPS | 95% pointwise HAC intervals, six lags | Full: Sep 2002–Nov 2021; evaluation: Feb 2016–Nov 2021", fontsize=9)
    fig.savefig(FIGURES / "incremental_alpha.png")
    plt.close(fig)


def main():
    RESULTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((ROOT / "data" / "source_manifest.json").read_text())
    for archive in [ARCHIVE, "Factor_Time_Series_LongShort.zip", "djm_data.zip"]:
        if hashlib.sha256((RAW/archive).read_bytes()).hexdigest() != manifest[archive]["sha256"]:
            raise ValueError(f"Source hash mismatch: {archive}")
    raw = {name: read_member(ARCHIVE, f"ExcessLongShortVW_{name}.csv") for name in ["DFPS", "OSBAP", "ICE"]}
    _, replication = reproduce_author_comparison(raw)
    selected, maps = {}, []
    quality = []
    for name, df in raw.items():
        selected[name], mapping = select_signals(df)
        maps.extend(dict(dataset=name, **r) for r in mapping)
        quality.append(dict(dataset=name, rows=len(df), factors=df.shape[1], start=str(df.index.min().date()),
                            end=str(df.index.max().date()), missing_all=int(df.isna().sum().sum()),
                            missing_selected=int(selected[name].isna().sum().sum()), duplicates=int(df.index.has_duplicates)))
    benchmark = read_member("djm_data.zip", "traded_bond_excess.csv", dayfirst=True)[["MKTB", "TERM"]]
    common = benchmark.dropna().index
    for df in selected.values():
        common = common.intersection(df.dropna().index)
    common = common.sort_values()
    if not common.to_period("M").equals(pd.period_range(common[0], common[-1], freq="M")):
        raise ValueError("The common sample is not contiguous")
    frames = {k: combine(v.loc[common]) for k, v in selected.items()}
    split = math.floor(.7*len(common))
    periods = {"Full": common, "Development": common[:split], "Evaluation": common[split:],
               "2013–2023 overlap": common[(common.year >= 2013) & (common.year <= 2023)]}
    summaries = []
    for name, df in frames.items():
        for sample, dates in periods.items():
            summaries.append(performance(df.loc[dates], benchmark, sample, name))
        df.to_csv(RESULTS/f"monthly_returns_{name.lower()}.csv", index_label="date")
    summary = pd.concat(summaries, ignore_index=True)
    summary.to_csv(RESULTS/"performance.csv", index=False)
    pd.DataFrame(maps).to_csv(RESULTS/"signal_mapping.csv", index=False)
    pd.DataFrame(quality).to_csv(RESULTS/"data_quality.csv", index=False)
    benchmark.loc[common].to_csv(RESULTS/"benchmarks.csv", index_label="date")
    frames["DFPS"][list(SIGNALS)].corr().to_csv(RESULTS/"signal_correlations.csv")

    # ICE duration adjustment is an explicitly separate sensitivity, not TRACE hedging.
    duration_raw = read_member("Factor_Time_Series_LongShort.zip", "DurAdjLongShortVW.csv")
    duration, duration_map = select_signals(duration_raw)
    pd.DataFrame(duration_map).to_csv(RESULTS/"duration_signal_mapping.csv", index=False)
    duration = combine(duration.loc[common])
    pd.concat([performance(duration.loc[dates], benchmark, sample, "ICE duration-adjusted")
               for sample, dates in periods.items()]).to_csv(RESULTS/"duration_sensitivity.csv", index=False)

    # Raw signed returns are displayed only as an orientation-bias diagnostic.
    signed = pd.DataFrame(index=common)
    for label, (base, _, _) in SIGNALS.items():
        col = next(c for c in raw["DFPS"] if c.rstrip("*") == base)
        signed[label] = raw["DFPS"].loc[common, col]
    direction_rows = []
    for label in list(SIGNALS)+COMPOSITES:
        a, b = combine(signed)[label], frames["DFPS"][label]
        direction_rows.append(dict(strategy=label, source_orientation_mean_pct=1200*a.mean(),
                                   economic_orientation_mean_pct=1200*b.mean(),
                                   source_orientation_sharpe=np.sqrt(12)*a.mean()/a.std(),
                                   economic_orientation_sharpe=np.sqrt(12)*b.mean()/b.std()))
    pd.DataFrame(direction_rows).to_csv(RESULTS/"orientation_sensitivity.csv", index=False)

    costs = []
    for sample, dates in periods.items():
        for strategy in COMPOSITES:
            y = frames["DFPS"].loc[dates, strategy]
            for hurdle in [0, 100, 200, 400]:
                costs.append(dict(sample=sample, strategy=strategy, annual_hurdle_bps=hurdle,
                                  annual_mean_after_hurdle_pct=1200*y.mean()-hurdle/100))
    pd.DataFrame(costs).to_csv(RESULTS/"cost_hurdles.csv", index=False)

    # Direct incremental-return inference and alternative HAC bandwidths.
    bandwidth = []
    for sample, dates in periods.items():
        for name in COMPOSITES+["Combined minus bond"]:
            for lag in [3, 6, 12]:
                reg = fit_hac(frames["DFPS"].loc[dates, name], benchmark.loc[dates], lag)
                bandwidth.append(dict(sample=sample, strategy=name, lags=lag,
                                      annual_alpha_pct=1200*reg.params[0], t=reg.tvalues[0], p=reg.pvalues[0]))
    pd.DataFrame(bandwidth).to_csv(RESULTS/"hac_sensitivity.csv", index=False)
    metadata = {"primary": "DFPS TRACE-derived factor returns; ICE/BAML bond signal inputs",
                "sample_start": str(common[0].date()), "sample_end": str(common[-1].date()),
                "months": len(common), "evaluation_start": str(common[split].date()),
                "development_months": split, "evaluation_months": len(common)-split,
                "replication": replication, "hac_lags": 6, "bh_family_size": len(frames["DFPS"].columns),
                "costs": "Uncalibrated annual hurdles, not estimated trading costs",
                "raw_sha256": {k: manifest[k]["sha256"] for k in [ARCHIVE, "Factor_Time_Series_LongShort.zip", "djm_data.zip"]}}
    (RESULTS/"study_metadata.json").write_text(json.dumps(metadata, indent=2)+"\n")
    from incremental import write_diagnostics
    write_diagnostics(frames, benchmark, periods, RESULTS)
    figures(frames["DFPS"], summary)
    print(json.dumps(metadata, indent=2))
    print(summary.query("dataset == 'DFPS' and strategy in @COMPOSITES")[["sample", "strategy", "annual_mean_pct", "sharpe", "market_term_alpha_pct", "market_term_alpha_p", "market_term_alpha_q"]].to_string(index=False))


if __name__ == "__main__":
    main()
