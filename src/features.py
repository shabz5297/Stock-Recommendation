'''
feature engineering from raw price data
'''
from pyexpat import features

import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)

class FeatureEngineer:

	def __init__(self, price_data: pd.DataFrame):
		self.price_data = price_data
		self.returns = np.log(price_data / price_data.shift(1))
		self.features = pd.DataFrame(index=price_data.index)
		self.features = pd.DataFrame(index=price_data.index)

	def momentum_indicators(self, window=10) -> pd.DataFrame:
		# calculate momentum(price change over N days)
		logger.info(f"Calculating momentum (window={window})...")

		# momentum
		self.features[f'momentum_{window}'] = self.returns.rolling(window).sum()

		# rate of change
		self.features[f"roc_{window}"] = (
		(self.price_data - self.price_data.shift(window)) /
		self.price_data.shift(window)
		)

		return self.features

	def mean_reversion_indicators(self) -> pd.DataFrame:
		# calculate mean reversion (far deviation from mean)

		logger.info("Calculating mean reversion indicators...")

		sma_20= self.price_data.rolling(20).mean()

		sma_50= self.price_data.rolling(50).mean()

		# price relative to moving avg
		self.features['price_to_sma20'] = self.price_data / sma_20
		self.features['price_to_sma50'] = self.price_data / sma_50

		# distance from moving avg (z-score)
		std_20 = self.price_data.rolling(20).std()
		self.features['z_score_20'] = (self.price_data - sma_20) / sma_20

		return self.features




	def engineer_all(self) -> pd.DataFrame:
		logger.info(f"Calculating engineering indicators...")

		self.momentum_indicators()
		self.mean_reversion_indicators()

		# drop NaN rows
		self.features = self.features.dropna()

		logger.info(f"✅ Generated {self.features.shape[1]} features")
		logger.info(f"Final shape: {self.features.shape}")

		return self.features

# Test it
if __name__ == "__main__":
	from data_fetch import StockDataFetcher
	from config import TICKERS, START_DATE, END_DATE

	# Load data
	handler = StockDataFetcher(TICKERS, START_DATE, END_DATE)
	prices = handler.fetch_price_data()
	handler.validate_data()

	# Engineer features
	engineer = FeatureEngineer(prices)
	features = engineer.engineer_all()

	print("\n✅ Features engineered successfully")
	print(f"Shape: {features.shape}")
	print(features.head())

	# Check for NaN
	print(f"\nNaN count: {features.isna().sum().sum()}")