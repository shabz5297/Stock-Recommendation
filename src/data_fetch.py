import time
import logging
from logging import basicConfig
import numpy as np
import pandas as pd
import requests
import yfinance as yf
from typing import Tuple, Dict

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

#event tracker
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StockDataFetcher:
	def __init__(self, tickers: list, start_date: str, end_date: str):
		self.tickers = tickers
		self.start_date = start_date
		self.end_date = end_date
		self.price_data = None
		self.fundamentals = None

	def fetch_price_data(self) -> pd.DataFrame:
		logger.info(f"Fetching price data for {len(self.tickers)} stocks...")
		try:
			data = yf.download(
				self.tickers,
				start=self.start_date,
			   	end=self.end_date,
			   	progress=False
			)

			if data.empty:
				raise ValueError("No data provided by Yahoo Finance.")

			time.sleep(1)  # rate limiting

			#Return only close prices
			if len(self.tickers) == 1:
				self.price_data = pd.DataFrame(
					data['Close'],
					columns=self.tickers
				)
			else:
				self.price_data = data['Close']

			logger.info(f"Downloaded {len(self.price_data)} trading days")

			return self.price_data

		except Exception as e:
			logger.error(f"Error fetching data: {e}")
			raise

	def fetch_fundamentals(self) -> pd.DataFrame:
			logger.info("Fetching fundamental data...")
			fundamentals = {}

			for i, ticker in enumerate(self.tickers):
				if i > 0:
					time.sleep(1)

				try:
					logger.info(f"   {ticker}...", end=" ")
					stock = yf.Ticker(ticker)
					info = stock.info

					#extract key attributes
					fundamentals[ticker] = {
						'pe_ratio': info.get('trailingPE'),
						'roe': info.get('returnOnEquity'),
						'debt_to_equity': info.get('debtTrEquity'),
						'profit_margin': info.get('profitMargins'),
						'market_cap': info.get('marketCap'),
						'dividend_yield': info.get('dividendYield'),
						'industry': info.get('industry'),
						'sector': info.get('sector')
					}
					logger.info("✔")

				except Exception as e:
					logger.warning(f"⚠ ️ Error fetching fundamentals for {ticker}: {e}")
					fundamentals[ticker] = {}

			self.fundamentals = pd.DataFrame(fundamentals).T
			logger.info("✔ Fundamentals fetched")
			return self.fundamentals

	def validate_data(self) -> bool:
		logger.info(f"Validating data...")

		if self.price_data is None:
			raise ValueError("No data provided by Yahoo Finance.")

			#check for missing values
		missing = self.price_data.isna().sum().sum()
		if missing > 0:
			logger.warning(f"Found {missing} missing values")
			#forward fill then backward fill
			self.price_data = self.price_data.fillna(method='ffill').fillna(method='bfill')

			# Check for negative prices (shouldn't happen)
			if (self.price_data < 0).any().any():
				raise ValueError("Negative prices found")

			# Check date range
			logger.info(f"Date range: {self.price_data.index[0]} to {self.price_data.index[-1]}")
			logger.info(f"Trading days: {len(self.price_data)}")

			return True

	def get_returns(self, method='log') -> pd.DataFrame:
		if self.price_data is None:
			raise ValueError("Price data not loaded")

		if method == 'log':
			returns = np.log(self.price_data / self.price_data.shift(1))
		else:
			returns = self.price_data.pct_change()

		return returns.dropna()

# Test it
if __name__ == "__main__":
	from config import TICKERS, START_DATE, END_DATE, BACKTEST_START
	handler = StockDataFetcher(TICKERS, START_DATE, END_DATE)

	# Fetch data
	prices = handler.fetch_price_data()
	print(f"\n ✔ Price data shape: {prices.shape}")
	print(prices.head())

	# Validate
	handler.validate_data()

	# Get returns
	returns = handler.get_returns()
	print(f"\n ✔ Returns shape: {returns.shape}")
	print(f"Mean daily return: {returns.mean().mean():.4%}")
	print(f"Daily volatility: {returns.std().mean():.4%}")