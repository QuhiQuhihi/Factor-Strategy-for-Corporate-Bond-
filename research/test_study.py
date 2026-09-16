"""Small, material checks for the research calculations; no live data required."""
import unittest
import numpy as np
import pandas as pd
from run_study import SIGNALS, combine, fit_hac, performance, select_signals


class StudyChecks(unittest.TestCase):
    def test_direction_is_independent_of_realized_mean(self):
        index = pd.date_range("2000-01-31", periods=2, freq="ME")
        df = pd.DataFrame(index=index)
        for name, (base, _, _) in SIGNALS.items():
            df[base + ("*" if name in ["Bond momentum", "Equity profitability"] else "")] = [.01, -.03]
        oriented, _ = select_signals(df)
        np.testing.assert_allclose(oriented["Bond momentum"], [-.01, .03])
        np.testing.assert_allclose(oriented["Low volatility"], [-.01, .03])
        np.testing.assert_allclose(oriented["Credit spread"], [.01, -.03])
        np.testing.assert_allclose(oriented["Equity profitability"], [-.01, .03])

    def test_missing_signal_cannot_change_weights(self):
        df = pd.DataFrame(np.zeros((3, 6)), columns=SIGNALS)
        df.iloc[0, 1] = np.nan
        with self.assertRaises(ValueError):
            combine(df)

    def test_ambiguous_source_column_rejected(self):
        with self.assertRaises(ValueError):
            select_signals(pd.DataFrame({"VW_18_spread": [1], "VW_18_spread*": [1]}))

    def test_combination_matches_hand_calculation(self):
        df = pd.DataFrame([[.06, -.03, 0, .12, .03, -.06]], columns=SIGNALS)
        result = combine(df).iloc[0]
        self.assertAlmostEqual(result["Bond-only"], .01)
        self.assertAlmostEqual(result["Equity-derived"], .03)
        self.assertAlmostEqual(result["Combined"], .02)
        self.assertAlmostEqual(result["Combined minus bond"], .01)

    def test_hac_matches_independent_matrix_calculation(self):
        rng = np.random.default_rng(441)
        x = pd.DataFrame(rng.normal(size=(80, 2)), columns=["MKTB", "TERM"])
        y = pd.Series(.3 + x.to_numpy() @ np.array([.5, -.2]) + rng.normal(size=80))
        design = np.column_stack([np.ones(80), x])
        beta = np.linalg.lstsq(design, y, rcond=None)[0]
        residual = y.to_numpy()-design@beta
        scores = design*residual[:, None]
        meat = scores.T@scores
        for lag in range(1, 7):
            cross = scores[lag:].T@scores[:-lag]
            meat += (1-lag/7)*(cross+cross.T)
        bread = np.linalg.inv(design.T@design)
        covariance = bread@meat@bread*80/(80-3)
        fit = fit_hac(y, x)
        np.testing.assert_allclose(fit.params, beta, atol=1e-12)
        np.testing.assert_allclose(fit.cov_params(), covariance, atol=1e-12)

    def test_rank_deficiency_rejected(self):
        x = pd.DataFrame({"a": np.arange(20), "b": np.arange(20)*2})
        with self.assertRaises(ValueError):
            fit_hac(pd.Series(np.arange(20)), x)

    def test_drawdown_includes_initial_loss(self):
        index = pd.date_range("2000-01-31", periods=20, freq="ME")
        y = pd.DataFrame({"test": [-.1] + [.001]*19}, index=index)
        rng = np.random.default_rng(23)
        b = pd.DataFrame(rng.normal(size=(20, 2)), index=index, columns=["MKTB", "TERM"])
        out = performance(y, b, "test", "synthetic unit check").iloc[0]
        self.assertAlmostEqual(out.max_pnl_drawdown_pct, -10)
        self.assertAlmostEqual(out.annual_mean_pct, 1200*(-.1+.019)/20)


if __name__ == "__main__":
    unittest.main()
