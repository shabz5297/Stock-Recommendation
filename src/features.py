'''
feature engineering from raw price data
'''

import pandas as pd
import numpy as np
import logging

logger.getLogger(__name__)

class FeatureEngineering:

	def __init__(self, price_data: pd.DataFrame):
		self.price_data = price_data
		self.returns = np.log(price_data / price_data.shift(1))
		self.features = pd.DataFrame(index=price_data.index)
		self.features = pd.DataFrame(index=price_data.index)