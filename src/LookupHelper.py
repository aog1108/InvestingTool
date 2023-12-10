import numpy as np
from numpy.lib.stride_tricks import sliding_window_view
from numba import jit
from numba import float64
from numba import int64

"""
data : numpy matrix(No 1d-array)
- The functions in this module must be implemented by numpy
- The functions should handle vectorized data along vertical axis 
- No error check(the error checking should be done outside) 
"""


def get_return(data, period):
    return np.apply_along_axis(lambda x: (x[period:] - x[:-period])/x[:-period], axis=0, arr=data)


def get_volatility(data, period):
    ret = get_return(data, 1)
    return np.apply_along_axis(lambda x: np.sqrt(252) * np.std(sliding_window_view(x, window_shape=period),
                                                               axis=1,
                                                               ddof=1),
                               axis=0,
                               arr=ret)


def get_standard_deviation(data, period):
    return np.apply_along_axis(lambda x: np.std(sliding_window_view(x, window_shape=period), axis=1, ddof=1),
                               axis=0,
                               arr=data)


def get_simple_moving_average(data, period):
    return np.apply_along_axis(lambda x: np.mean(sliding_window_view(x, window_shape=period), axis=1), axis=0, arr=data)


def get_exponential_moving_average(data, period):
    return np.apply_along_axis(lambda x: _ewma_infinite_hist(x, period), axis=0, arr=data)


def get_upper_bollinger_band(data, ma_period, std_period, sigma_level):
    ma = get_simple_moving_average(data, ma_period)
    std = get_standard_deviation(data, std_period)
    length = min(len(ma), len(std))
    return ma[max(len(ma) - length, 0):, :] + sigma_level * std[max(len(std) - length, 0):, :]


def get_lower_bollinger_band(data, ma_period, std_period, sigma_level):
    ma = get_simple_moving_average(data, ma_period)
    std = get_standard_deviation(data, std_period)
    length = min(len(ma), len(std))
    return ma[max(len(ma) - length, 0):, :] - sigma_level * std[max(len(std) - length, 0):, :]


def get_percent_b(data, ma_period, std_period, sigma_level):
    upper_band = get_upper_bollinger_band(data, ma_period, std_period, sigma_level)
    lower_band = get_lower_bollinger_band(data, ma_period, std_period, sigma_level)
    return (data[len(data) - len(upper_band):, :] - lower_band) / (upper_band - lower_band)


def get_bandwidth(data, ma_period, std_period, sigma_level):
    upper_band = get_upper_bollinger_band(data, ma_period, std_period, sigma_level)
    lower_band = get_lower_bollinger_band(data, ma_period, std_period, sigma_level)
    mid_band = get_simple_moving_average(data, ma_period)
    length = min(len(upper_band), len(mid_band))
    return (upper_band[max(len(upper_band) - length, 0):, :] - lower_band[max(len(lower_band) - length, 0):, :]) \
           / mid_band[max(len(mid_band) - length, 0):, :]


def get_rsi(data, period):
    diff = np.apply_along_axis(lambda x: x[1:] - x[:-1], axis=0, arr=data)
    u = np.maximum(diff, 0)
    d = np.maximum(-diff, 0)
    au = get_simple_moving_average(u, period)
    ad = get_simple_moving_average(d, period)
    rs = au / ad
    return 100 - 100 / (1 + rs)


def get_rolling_max(data, period):
    return np.apply_along_axis(lambda x: np.max(sliding_window_view(x, window_shape=period), axis=1), axis=0, arr=data)


def get_rolling_min(data, period):
    return np.apply_along_axis(lambda x: np.min(sliding_window_view(x, window_shape=period), axis=1), axis=0, arr=data)


def get_max(data):
    max_values = np.max(data, axis=0)
    return np.repeat(max_values[np.newaxis, :], len(data), 0)


def get_min(data):
    min_values = np.min(data, axis=0)
    return np.repeat(min_values[np.newaxis, :], len(data), 0)


@jit((float64[:], int64), nopython=True, nogil=True)
def _ewma_infinite_hist(arr_in, window):
    n = arr_in.shape[0]
    ewma = np.empty(n, dtype=float64)
    alpha = 2 / float(window + 1)
    ewma[0] = arr_in[0]
    for i in range(1, n):
        ewma[i] = arr_in[i] * alpha + ewma[i - 1] * (1 - alpha)
    return ewma
