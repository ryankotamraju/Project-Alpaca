This project is a pairs trading algorithm implemented for taking long and short positions on the stocks VOO (Vanguard S&P 500 ETF) and QQQ (Invesco QQQ Trust). Developed as a submission for a Quantitative Portfolio Management and Algorithmic Trading class, this algorithm uses statistical arbitrage to capitalize on temporary divergences in price between the two highly correlated ETFs.

# Project Overview
Pairs trading is a market-neutral trading strategy that seeks to profit from the relative price movements between two correlated assets. This algorithm identifies opportunities to go long on one ETF and short on the other when they deviate from their historical relationship, expecting them to converge over time.

# Key Features
Spread Calculation: Calculates the spread between VOO and QQQ to identify trading signals.
Mean Reversion: Uses mean reversion principles to predict convergence, assuming the spread will revert to its historical mean.
Trading Signals: Generates buy and sell signals for long and short positions based on z-scores of the spread.
Risk Management: Includes risk controls for position sizing, stop-loss, and take-profit limits.
Backtesting: Tested on historical data to evaluate performance, with key metrics such as cumulative returns, Sharpe ratio, and maximum drawdown.

# Methodology
- Data Collection: Historical price data for VOO and QQQ is used to calculate the spread.
- Spread Calculation: Computes the spread as the difference in price between the two ETFs.
- Z-Score Normalization: Normalizes the spread using a z-score to identify extreme deviations from the mean.
- Signal Generation:
  - Go Long: If the z-score of the spread falls below a specified threshold (e.g., -2), indicating VOO is undervalued relative to QQQ.
  - Go Short: If the z-score rises above a threshold (e.g., +2), indicating VOO is overvalued relative to QQQ.
- Position Management: Holds positions until the z-score reverts to a specified threshold near zero.
- Risk Management: Implements stop-loss and take-profit rules to mitigate risk.

# Getting Started
## Prerequisites
Python 3.x
Libraries: pandas, time, alpaca for data collection, analysis, strategy implementation, and trading.

# Usage
Run the Algorithm: Use main.py to initialize and execute the trading strategy.
Configure Parameters: Edit the script to set trading thresholds, lookback period, and position sizing.

# Limitations and Assumptions
- Market Neutral Assumption: Assumes that VOO and QQQ have a long-term mean-reverting relationship.
- Stationarity: The strategy relies on the spread’s stationarity; deviations from this assumption can impact performance.
- Transaction Costs: This backtest does not account for transaction costs, which can affect net profitability.

# Contributions
This project was developed as an academic submission, but contributions are welcome for improvements or additional features. To contribute, fork the repository, make your changes, and submit a pull request.

# License
This project is licensed under the MIT License.

Acknowledgments
Special thanks to the *FINM 25000 Quantitative Portfolio Management and Algorithmic Trading* faculty Mark Hendricks and Sebastien Donadio and for their support and guidance in the development of this project, as well as classmates Keira Wang, Sebastian Tchkotoua, and Andrew Moukabary for their contributions to this collaborative project.
