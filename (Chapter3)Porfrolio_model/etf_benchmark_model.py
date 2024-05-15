import os
import sys
import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

class etf_benchmark:
    def __init__(self):
        self.start_date = '20140501'
        self.eval_date = '20240501'
        print("current dir is : ", os.getcwd())
        self.main_dir = os.path.join("C:\\", 'workspace', 'Factor-Strategy-for-Corporate-Bond-')
        print("main dir is : ", self.main_dir)
        self.data_dir = os.path.join(self.main_dir, "(Chapter1)Data")
        print("data dir is : ", self.data_dir)

        # Load the ETF data
        self.data = pd.read_csv(os.path.join(self.data_dir, 'etf_data_result.csv'), index_col='Date', parse_dates=True)

        # Select only the adjusted return columns
        self.return_columns = [col for col in self.data.columns if 'Adjusted_Return' in col]
        self.returns = self.data[self.return_columns]

    # Helper function to calculate portfolio returns
    def portfolio_returns(self, weights, returns):
        return np.dot(returns, weights)

    # Helper function to calculate portfolio volatility
    def portfolio_volatility(self, weights, cov_matrix):
        return np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))


    def mean_variance_optimization(self, returns):
        mean_returns = returns.mean()
        cov_matrix = returns.cov()
        def objective(weights):
            return -self.portfolio_returns(weights, mean_returns) / self.portfolio_volatility(weights, cov_matrix)
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bounds = tuple((0.05, 0.5) for _ in range(len(mean_returns)))  # Each ETF has at least 5% and no more than 50% weight
        initial_guess = [1. / len(mean_returns)] * len(mean_returns)
        result = minimize(objective, initial_guess, method='SLSQP', bounds=bounds, constraints=constraints)
        return result.x
    
    def risk_parity_optimization(self, returns):
        cov_matrix = returns.cov()
        def objective(weights):
            return self.portfolio_volatility(weights, cov_matrix)
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bounds = tuple((0.05, 0.5) for _ in range(len(returns.columns)))  # Each ETF has at least 5% and no more than 50% weight
        initial_guess = [1. / len(returns.columns)] * len(returns.columns)
        result = minimize(objective, initial_guess, method='SLSQP', bounds=bounds, constraints=constraints)
        return result.x


    def simulate_portfolio(self, data, window=8):
        portfolio_weights_mv = []
        portfolio_weights_rp = []
        portfolio_weights_1n = []

        num_assets = len(data.columns)
        asset_names = data.columns  # Assuming the columns in 'data' are named after the ETFs

        for i in range(window, len(data)):
            current_returns = data.iloc[i-window:i]
            weights_mv = self.mean_variance_optimization(current_returns)
            weights_rp = self.risk_parity_optimization(current_returns)
            weights_1n = np.array([1 / num_assets] * num_assets)

            portfolio_weights_mv.append(weights_mv)
            portfolio_weights_rp.append(weights_rp)
            portfolio_weights_1n.append(weights_1n)

        weights_mv_df = pd.DataFrame(portfolio_weights_mv, index=data.index[window:], columns=asset_names)
        weights_rp_df = pd.DataFrame(portfolio_weights_rp, index=data.index[window:], columns=asset_names)
        weights_1n_df = pd.DataFrame(portfolio_weights_1n, index=data.index[window:], columns=asset_names)

        return weights_mv_df, weights_rp_df, weights_1n_df
    
    # def calculate_cumulative_returns(self, weights_df):
    #     # Ensure that the columns of weights_df match those in self.returns
    #     aligned_returns = self.returns.loc[weights_df.index, weights_df.columns]
        
    #     # Multiply weights by returns
    #     periodic_returns = weights_df.dot(aligned_returns.T).T
        
    #     # Calculate cumulative returns
    #     cumulative_returns = (1 + periodic_returns).cumprod() - 1
        
    #     return cumulative_returns
    
    def calculate_cumulative_returns(self, weights_df):
        # Ensure that the columns of weights_df match those in self.returns
        aligned_returns = self.returns.loc[weights_df.index, weights_df.columns]
        
        # Multiply weights by returns to get portfolio returns for each period
        portfolio_returns = (weights_df * aligned_returns).sum(axis=1)
        
        # Calculate cumulative returns, using a method that accounts for compounding
        cumulative_returns = (1 + portfolio_returns).cumprod() - 1

        return cumulative_returns

    def run(self):
        # Simulate the portfolios
        weights_mv_df, weights_rp_df, weights_1n_df = self.simulate_portfolio(self.returns)

        weights_mv_df.to_csv('weights_mv_df.csv')
        weights_rp_df.to_csv('weights_rp_df.csv')
        weights_1n_df.to_csv('weights_1n_df.csv')

        cumulative_returns_mv = self.calculate_cumulative_returns(weights_mv_df)
        cumulative_returns_rp = self.calculate_cumulative_returns(weights_rp_df)
        cumulative_returns_1n = self.calculate_cumulative_returns(weights_1n_df)

        # Combine all cumulative returns into one DataFrame for plotting
        cumulative_returns_all = pd.DataFrame({
            'Mean-Variance': cumulative_returns_mv,
            'Risk-Parity': cumulative_returns_rp,
            'Equal-Weight': cumulative_returns_1n
        })

        cumulative_returns_all.to_csv("cumulative_returns_all.csv")

        # Visualization of Portfolio Weights
        weights_mv_df.plot(title='Mean-Variance Optimization Weights')
        plt.legend()
        plt.show()

        weights_rp_df.plot(title='Risk Parity Optimization Weights')
        plt.legend()
        plt.show()

        weights_1n_df.plot(title='1/N Strategy Weights')
        plt.legend()
        plt.show()

        # Visualization of Cumulative Returns for all strategies on a log scale
        plt.figure()
        cumulative_returns_all.plot(title='Cumulative Returns - All Strategies', logy=False)
        plt.xlabel('Date')
        plt.ylabel('Cumulative Return')
        plt.legend()
        plt.show()
        # no log return since backtest period is relatively short

if __name__ == '__main__':
    run = etf_benchmark()
    run.run()