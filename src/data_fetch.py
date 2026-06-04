import yfinance as yf
import pandas as pd

class StockDataFetcher:
	def __init__(self, tickers, start_date, end_date):
		self.tickers = tickers
		self.start_date = start_date
		self.end_date = end_date

	def fetch_price_data(self):

		headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
		}

	#download price data for all tickers
		data = yf.download(tickers=self.tickers,
						   start=self.start_date,
						   end=self.end_date,
						   progress=False
						   )
		#Return only close prices
		if len(self.tickers) == 1:
			return pd.DataFrame(data['Close'], columns=self.tickers)
		else:
			return data['Close']

	def fetch_fundamentals(self):
		fundamentals = {}

		for ticker in self.tickers:
			try:
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
			except Exception as e:
				print(f"⚠ ️ Error fetching fundamentals for {ticker}: {e}")
				fundamentals[ticker] = {}

		return pd.DataFrame(fundamentals).T

	def get_stock_info(self, ticker):
		stock=yf.Ticker(ticker)
		info = stock.info

		return {
		'name': info.get('longName'),
		'sector': info.get('sector'),
		'industry': info.get('industry'),
		'market_cap': info.get('marketCap'),
		'fifty_two_week_high': info.get('fiftyTwoWeekHigh'),
		'fifty_two_week_low': info.get('fiftyTwoWeekLow'),
		'current_price': info.get('currentPrice')
		}


if __name__ == '__main__':
	fetcher = StockDataFetcher(
	tickers=['AAPL'],
	start_date='2022-01-01',
	end_date='2024-05-01'
	)

	#fetch data
	print("fetching data..")
	price_data = fetcher.fetch_price_data()
	print(f"Downloaded  {price_data.shape[0]} rows x {price_data.shape[1]} stocks")

	print("\nFirst 5 rows:")
	print(price_data.head())

	#fetch fundamentals
	print("\nFetching Fundamentals..")
	fundamentals = fetcher.fetch_fundamentals()
	print("fundamentals fetched:")
	print(fundamentals)