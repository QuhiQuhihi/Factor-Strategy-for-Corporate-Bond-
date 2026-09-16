"""Material checks for temporal leakage, conditional alpha and paired inference."""
import unittest

import numpy as np
import pandas as pd

from incremental import CONTROL, TARGETS, cost_budget, risk_control, sharpe_interval, spanning
from run_study import SIGNALS, combine


class IncrementalChecks(unittest.TestCase):
    def setUp(self):
        rng = np.random.default_rng(781)
        self.dates = pd.date_range("2000-01-31", periods=100, freq="ME")
        self.frame = combine(pd.DataFrame(rng.normal(0, .02, (100, 6)),
                                          columns=SIGNALS, index=self.dates))
        self.benchmark = pd.DataFrame(rng.normal(0, .02, (100, 2)),
                                      columns=["MKTB", "TERM"], index=self.dates)

    def test_current_and_future_returns_cannot_change_current_weight(self):
        baseline = risk_control(self.frame)
        altered = self.frame.copy()
        altered.iloc[75:] *= 100
        changed = risk_control(altered)
        pd.testing.assert_series_equal(baseline.bond_weight.loc[:self.dates[75]],
                                       changed.bond_weight.loc[:self.dates[75]])
        self.assertEqual(baseline.training_end.iloc[0], self.dates[59])
        prior = self.frame.iloc[:60]
        weight = min(1, np.std(prior.Combined, ddof=1)/np.std(prior["Bond-only"], ddof=1))
        self.assertAlmostEqual(baseline.bond_weight.iloc[0], weight)
        self.assertAlmostEqual(baseline[CONTROL].iloc[0], weight*self.frame["Bond-only"].iloc[60])

    def test_scaling_cap_and_warmup(self):
        self.frame["Combined"] = 2*self.frame["Bond-only"]
        out = risk_control(self.frame)
        self.assertEqual(len(out), 40)
        np.testing.assert_allclose(out.bond_weight, 1)
        np.testing.assert_allclose(out[CONTROL], out["Bond-only"])

    def test_missing_month_and_zero_volatility_rejected(self):
        with self.assertRaises(ValueError):
            risk_control(self.frame.drop(self.dates[5]))
        self.frame["Bond-only"] = 0
        with self.assertRaises(ValueError):
            risk_control(self.frame)

    def test_conditional_alpha_matches_independent_partial_regression(self):
        # Frisch-Waugh-Lovell: residualize the intercept and target on controls.
        x = pd.concat([self.frame[list(SIGNALS)[:3]], self.benchmark], axis=1).to_numpy()
        one = np.ones(len(x))
        residual_intercept = one-x@np.linalg.lstsq(x, one, rcond=None)[0]
        out = spanning(self.frame, self.benchmark).set_index("target")
        for target in TARGETS:
            y = self.frame[target].to_numpy()
            residual_target = y-x@np.linalg.lstsq(x, y, rcond=None)[0]
            alpha = residual_intercept@residual_target/(residual_intercept@residual_intercept)
            self.assertAlmostEqual(out.loc[target, "annual_alpha_pct"], 1200*alpha)

    def test_misaligned_benchmark_rejected(self):
        with self.assertRaises(ValueError):
            spanning(self.frame, self.benchmark.iloc[::-1])

    def test_paired_bootstrap_identical_paths_have_zero_difference(self):
        y = self.frame.Combined.to_numpy()
        out = sharpe_interval(y, y, block=6, draws=100)
        np.testing.assert_allclose([out["sharpe_difference"], out["ci_low"], out["ci_high"]], 0)

    def test_full_length_circular_blocks_preserve_sharpes(self):
        candidate = self.frame.Combined.to_numpy()
        control = self.frame["Bond-only"].to_numpy()
        out = sharpe_interval(candidate, control, block=len(candidate), draws=100)
        expected = np.sqrt(12)*(candidate.mean()/candidate.std(ddof=1)-control.mean()/control.std(ddof=1))
        np.testing.assert_allclose([out["sharpe_difference"], out["ci_low"], out["ci_high"]], expected)

    def test_negative_cost_headroom_is_not_clipped(self):
        out = cost_budget(pd.Series(np.full(80, -.001)))
        self.assertAlmostEqual(out["annual_incremental_mean_bps"], -120)
        self.assertLess(out["ci_high_bps"], 0)
        self.assertEqual(out["materiality_assessment"], "Below illustrative threshold")


if __name__ == "__main__":
    unittest.main()
