import numpy as np
import pandas as pd


def data_type_check(data):
    if type(data) != pd.DataFrame:
        raise RuntimeError("Data type should be the DataFrame")


def data_column_len_check(data):
    if len(data.columns) != 1:
        raise RuntimeError("Data should have only one column")


def simple_moving_average(data, ma_period):
    sma = data.rolling(ma_period).mean()
    return sma


def exponential_moving_average(data, ma_period):
    ema = data.ewm(span=ma_period, adjust=False).mean()
    return ema


def weighted_moving_average(data, ma_period):
    w = np.arange(1, ma_period + 1)
    wma = data.rolling(ma_period).apply(lambda x: (w * x).sum() / w.sum(), raw=True)
    return wma
