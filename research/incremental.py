"""Exploratory allocation diagnostics; see the dated amendment in PROTOCOL.md."""
from __future__ import annotations

import hashlib
from itertools import combinations
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import norm
from statsmodels.stats.multitest import multipletests

from run_study import SIGNALS, fit_hac

LOOKBACK = 60
BOOTSTRAP_DRAWS = 5000
SEED = 20260916
MATERIALITY_BPS = 50
CONTROL = "Risk-scaled bond"
TARGETS = ["Equity-derived", *list(SIGNALS)[3:]]


def check_panel(frame: pd.DataFrame) -> None:
    if not isinstance(frame.index, pd.DatetimeIndex) or frame.index.empty:
        raise ValueError("Expected a nonempty monthly date index")
    months = frame.index.to_period("M")
    if not months.equals(pd.period_range(months[0], months[-1], freq="M")):
        raise ValueError("Expected unique, sorted, contiguous monthly observations")
    if not np.isfinite(frame.to_numpy()).all():
        raise ValueError("Missing or nonfinite observations in diagnostic panel")


def spanning(frame: pd.DataFrame, benchmark: pd.DataFrame, lags: int = 6) -> pd.DataFrame:
    """Conditional alpha, not the joint restrictions of a full spanning test."""
    check_panel(frame)
    if not benchmark.index.equals(frame.index):
        raise ValueError("Benchmark dates must match target dates exactly")
    check_panel(benchmark)
    controls = pd.concat([frame[list(SIGNALS)[:3]], benchmark[["MKTB", "TERM"]]], axis=1)
    standardized = (controls-controls.mean())/controls.std(ddof=1)
    condition = np.linalg.cond(np.column_stack([np.ones(len(frame)), standardized]))
    rows = []
    for target in TARGETS:
        fit = fit_hac(frame[target], controls, lags)
        alpha, se = fit.params[0]*1200, fit.bse[0]*1200
        rows.append(dict(target=target, n=len(frame), lags=lags, annual_alpha_pct=alpha,
                         alpha_ci_low_pct=alpha-1.96*se, alpha_ci_high_pct=alpha+1.96*se,
                         alpha_p=fit.pvalues[0], r_squared=fit.rsquared,
                         residual_annual_vol_pct=np.std(fit.resid, ddof=1)*np.sqrt(12)*100,
                         standardized_design_condition=condition))
    out = pd.DataFrame(rows)
    out["alpha_q"] = multipletests(out.alpha_p, method="fdr_bh")[1]
    return out


def risk_control(frame: pd.DataFrame, lookback: int = LOOKBACK) -> pd.DataFrame:
    check_panel(frame)
    if lookback < 2 or len(frame) <= lookback:
        raise ValueError("Need at least two training months and one later observation")
    vol = frame[["Bond-only", "Combined"]].rolling(lookback).std(ddof=1).shift(1)
    prior = vol.iloc[lookback:]
    if (prior["Bond-only"] <= 0).any():
        raise ValueError("Cannot scale a control with zero estimated bond volatility")
    ratio = prior["Combined"]/prior["Bond-only"]
    out = frame.loc[prior.index, ["Bond-only", "Combined"]].copy()
    out["unclipped_bond_weight"] = ratio
    out["bond_weight"] = ratio.clip(0, 1)
    out[CONTROL] = out["bond_weight"]*out["Bond-only"]
    out["training_end"] = frame.index[lookback-1:-1]
    return out


def sharpe_interval(candidate: np.ndarray, control: np.ndarray, block: int,
                    draws: int = BOOTSTRAP_DRAWS, seed: int = SEED) -> dict:
    """Paired circular-block percentile interval, conditional on realized paths."""
    pair = np.column_stack([candidate, control])
    n = len(pair)
    if not 1 <= block <= n or draws < 2 or not np.isfinite(pair).all():
        raise ValueError("Invalid paired bootstrap inputs")
    if np.any(pair.std(axis=0, ddof=1) <= 0):
        raise ValueError("Sharpe ratio requires positive sample volatility")
    rng = np.random.default_rng(seed)
    starts = rng.integers(0, n, size=(draws, int(np.ceil(n/block))))
    indices = ((starts[:, :, None]+np.arange(block)) % n).reshape(draws, -1)[:, :n]
    sample = pair[indices]
    deviations = sample.std(axis=1, ddof=1)
    if (deviations <= 0).any():
        raise ValueError("Degenerate bootstrap sample: no finite Sharpe ratio")
    ratios = np.sqrt(12)*sample.mean(axis=1)/deviations
    difference = ratios[:, 0]-ratios[:, 1]
    actual = np.sqrt(12)*pair.mean(axis=0)/pair.std(axis=0, ddof=1)
    return dict(sharpe_difference=actual[0]-actual[1],
                ci_low=float(np.quantile(difference, .025)),
                ci_high=float(np.quantile(difference, .975)),
                block_months=block, draws=draws, seed=seed)


def cost_budget(difference: pd.Series) -> dict:
    fit = fit_hac(difference)
    mean, se = fit.params[0]*120000, fit.bse[0]*120000
    low, high = mean-1.96*se, mean+1.96*se
    if low > MATERIALITY_BPS:
        assessment = "Above illustrative threshold"
    elif high < MATERIALITY_BPS:
        assessment = "Below illustrative threshold"
    else:
        assessment = "Inconclusive at illustrative threshold"
    return dict(annual_incremental_mean_bps=mean, ci_low_bps=low, ci_high_bps=high,
                mean_p=fit.pvalues[0], materiality_bps=MATERIALITY_BPS,
                materiality_assessment=assessment,
                approximate_mde_80pct_bps=(norm.ppf(.975)+norm.ppf(.8))*se)


def write_diagnostics(frames: dict[str, pd.DataFrame], benchmark: pd.DataFrame,
                      periods: dict[str, pd.DatetimeIndex], results: Path) -> None:
    span_rows, performance_rows, interval_rows, budget_rows = [], [], [], []
    for dataset, frame in frames.items():
        for sample in ["Full", "Development", "Evaluation"]:
            dates = periods[sample]
            for lag in [3, 6, 12]:
                span_rows.append(spanning(frame.loc[dates], benchmark.loc[dates], lag)
                                 .assign(dataset=dataset, sample=sample))
        controlled = risk_control(frame)
        controlled.to_csv(results/f"risk_control_returns_{dataset.lower()}.csv", index_label="date")
        control_periods = {"Post-warmup": controlled.index,
                           "Evaluation": controlled.index.intersection(periods["Evaluation"])}
        for sample, dates in control_periods.items():
            part = controlled.loc[dates]
            identity = dict(dataset=dataset, sample=sample, n=len(part),
                            start=dates[0].strftime("%Y-%m"), end=dates[-1].strftime("%Y-%m"))
            for strategy in ["Combined", "Bond-only", CONTROL]:
                y = part[strategy]
                performance_rows.append(dict(**identity, strategy=strategy,
                    annual_mean_pct=y.mean()*1200,
                    annual_vol_pct=y.std(ddof=1)*np.sqrt(12)*100,
                    sharpe=y.mean()/y.std(ddof=1)*np.sqrt(12),
                    mean_bond_weight=part.bond_weight.mean() if strategy == CONTROL else np.nan,
                    capped_months=int((part.unclipped_bond_weight > 1).sum()) if strategy == CONTROL else 0))
            for control in ["Bond-only", CONTROL]:
                budget_rows.append(dict(**identity, control=control,
                                        **cost_budget(part.Combined-part[control])))
                for block in [6, 12]:
                    interval_rows.append(dict(**identity, control=control,
                        **sharpe_interval(part.Combined.to_numpy(), part[control].to_numpy(), block)))
    pd.concat(span_rows, ignore_index=True).to_csv(results/"incremental_spanning.csv", index=False)
    pd.DataFrame(performance_rows).to_csv(results/"risk_control_performance.csv", index=False)
    pd.DataFrame(interval_rows).to_csv(results/"sharpe_difference_intervals.csv", index=False)
    pd.DataFrame(budget_rows).to_csv(results/"incremental_cost_budget.csv", index=False)

    source_rows = []
    for sample in ["Full", "Evaluation"]:
        sample_rows = []
        for a, b in combinations(frames, 2):
            dates = periods[sample]
            y = frames[a].loc[dates, "Combined"]-frames[b].loc[dates, "Combined"]
            fit = fit_hac(y)
            mean, se = fit.params[0]*120000, fit.bse[0]*120000
            sample_rows.append(dict(sample=sample, source_a=a, source_b=b, n=len(y),
                annual_mean_a_minus_b_bps=mean, ci_low_bps=mean-1.96*se,
                ci_high_bps=mean+1.96*se, mean_p=fit.pvalues[0],
                monthly_correlation=frames[a].loc[dates, "Combined"].corr(frames[b].loc[dates, "Combined"])))
        out = pd.DataFrame(sample_rows)
        out["mean_q"] = multipletests(out.mean_p, method="fdr_bh")[1]
        source_rows.append(out)
    pd.concat(source_rows, ignore_index=True).to_csv(results/"paired_source_differences.csv", index=False)
    root = Path(__file__).resolve().parent
    metadata = dict(amendment_date="2026-09-16", status="Exploratory; original results already inspected",
                    lookback_months=LOOKBACK, bootstrap_draws=BOOTSTRAP_DRAWS, seed=SEED,
                    bootstrap_block_months=[6, 12], primary_hac_lags=6,
                    spanning_family_size=4, materiality_bps=MATERIALITY_BPS,
                    protocol_sha256=hashlib.sha256((root/"PROTOCOL.md").read_bytes()).hexdigest(),
                    code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                    source_metadata="study_metadata.json",
                    inference_limits="Pointwise/defined-family inference; no correction for historical research selection")
    (results/"incremental_metadata.json").write_text(json.dumps(metadata, indent=2)+"\n")
