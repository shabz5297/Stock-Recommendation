"""
Configuration and constants for the stock recommendation engine
"""

# Data parameters
TICKERS = ['NOW', 'CSCO', 'EQIX', 'NVDA', 'APLD', 'NBIS', 'NVTS', 'WULF']
START_DATE = '2026-05-01'
END_DATE = '2026-06-01'
BACKTEST_START = '2025-05-01'  # Start backtesting from this date

# Feature parameters
RSI_PERIOD = 14
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9
BB_PERIOD = 20
BB_STD = 2

# Signal thresholds
RSI_OVERSOLD = 30
RSI_OVERBOUGHT = 70
MOMENTUM_WINDOW = 10

# Portfolio parameters
TARGET_VOLATILITY = 0.15  # 15% annual volatility target
MIN_POSITION = 0.01  # Minimum 1% in any stock
MAX_POSITION = 0.20  # Maximum 20% in any stock
REBALANCE_FREQUENCY = 'M'  # Monthly rebalancing

# Backtesting parameters
INITIAL_CAPITAL = 100_000
TRANSACTION_COST = 0.001  # 10 basis points (0.1%)
SLIPPAGE = 0.0005  # 5 basis points (0.05%)
RISK_FREE_RATE = 0.05  # 5% annual

# Analysis parameters
CONFIDENCE_LEVEL = 0.95
LOOKBACK_WINDOW = 252  # Trading days in a year