import unittest
import sys

sys.path.append('C:/Users/JeonSeongHun/PycharmProjects/TechnicalBacktesting')


if True:  # noqa: E402
    from LookupHelper import *
    from TechnicalIndicator import *
    from TestData import *
    import numpy as np
    from time import time
    from functools import partial


class LookupHelperUnitTest(unittest.TestCase):
    def test_return_is_valid(self):
        data = get_test_data()

        return_period = 1
        calcaulated_by_indicator = np.zeros(shape=(len(data) - return_period, len(data.columns)))

        def get_indicator(data, period):  # noqa : E306
            return Return(data, period)

        func = partial(get_indicator, period=return_period)
        indicator_name = 'RETURN ' + str(return_period)
        get_result_from_indicator(data, calcaulated_by_indicator, func, indicator_name)

        np_data = data.values
        np_calculated = get_return(np_data, return_period)

        self.assertTrue(np.isclose(calcaulated_by_indicator, np_calculated, atol=10e-13).sum() == np_calculated.size)

    def test_return_runtime(self):
        data = get_test_data()
        np_data = data.values

        ret = []
        return_period = 1
        def fun():  # noqa : E306
            nonlocal ret
            ret = get_return(np_data, return_period)

        measure_runtime(100, fun)
        self.assertIsInstance(ret, np.ndarray)

    def test_volatility_is_valid(self):
        data = get_test_data()

        vol_period = 20
        calcaulated_by_indicator = np.zeros(shape=(len(data) - vol_period, len(data.columns)))

        def get_indicator(data, period):  # noqa : E306
            return Volatility(data, period)

        func = partial(get_indicator, period=vol_period)
        indicator_name = 'VOLATILITY ' + str(vol_period)
        get_result_from_indicator(data, calcaulated_by_indicator, func, indicator_name)

        np_data = data.values
        np_calculated = get_volatility(np_data, vol_period)

        self.assertTrue(np.isclose(calcaulated_by_indicator, np_calculated, atol=10e-13).sum() == np_calculated.size)

    def test_volatility_runtime(self):
        data = get_test_data()
        np_data = data.values

        ret = []
        vol_period = 20
        def fun():  # noqa : E306
            nonlocal ret
            ret = get_volatility(np_data, vol_period)

        measure_runtime(100, fun)
        self.assertIsInstance(ret, np.ndarray)

    def test_simple_ma_is_valid(self):
        data = get_test_data()

        ma_period = 20
        calcaulated_by_indicator = np.zeros(shape=(len(data) - ma_period + 1, len(data.columns)))

        def get_indicator(data, period):  # noqa : E306
            return MovingAverage(data, period, 0)

        func = partial(get_indicator, period=ma_period)
        indicator_name = 'MA ' + str(ma_period)
        get_result_from_indicator(data, calcaulated_by_indicator, func, indicator_name)

        np_data = data.values
        np_calculated = get_simple_moving_average(np_data, ma_period)

        self.assertTrue(np.isclose(calcaulated_by_indicator, np_calculated, atol=10e-13).sum() == np_calculated.size)

    def test_simple_ma_runtime(self):
        data = get_test_data()
        np_data = data.values

        ret = []
        ma_period = 20
        def fun():  # noqa : E306
            nonlocal ret
            ret = get_simple_moving_average(np_data, ma_period)

        measure_runtime(100, fun)
        self.assertIsInstance(ret, np.ndarray)

    def test_exponential_ma_is_valid(self):
        data = get_test_data()

        ma_period = 20
        calcaulated_by_indicator = np.zeros(shape=(len(data), len(data.columns)))

        def get_indicator(data, period):  # noqa : E306
            return MovingAverage(data, period, 1)

        func = partial(get_indicator, period=ma_period)
        indicator_name = 'MA ' + str(ma_period)
        get_result_from_indicator(data, calcaulated_by_indicator, func, indicator_name)

        np_data = data.values
        np_calculated = get_exponential_moving_average(np_data, ma_period)

        self.assertTrue(np.isclose(calcaulated_by_indicator, np_calculated, atol=10e-13).sum() == np_calculated.size)

    def test_exponential_ma_runtime(self):
        data = get_test_data()
        np_data = data.values

        ret = []
        ma_period = 20
        def fun():  # noqa : E306
            nonlocal ret
            ret = get_exponential_moving_average(np_data, ma_period)

        measure_runtime(100, fun)
        self.assertIsInstance(ret, np.ndarray)

    def test_upper_bolliger_band_is_valid(self):
        data = get_test_data()

        ma_period = 25
        vol_period = 20
        sigma_level = 2
        calcaulated_by_indicator = np.zeros(shape=(len(data) - max(ma_period - 1, vol_period - 1), len(data.columns)))

        def get_indicator(data, ma_period, vol_period, sigma_level):  # noqa : E306
            return BollingerBand(data, ma_period, vol_period, sigma_level)

        func = partial(get_indicator, ma_period=ma_period, vol_period=vol_period, sigma_level=sigma_level)
        indicator_name = 'UBAND'
        get_result_from_indicator(data, calcaulated_by_indicator, func, indicator_name)

        np_data = data.values
        np_calculated = get_upper_bollinger_band(np_data, ma_period, vol_period, sigma_level)

        self.assertTrue(np.isclose(calcaulated_by_indicator, np_calculated, atol=10e-13).sum() == np_calculated.size)

    def test_upper_bollinger_band_runtime(self):
        data = get_test_data()
        np_data = data.values

        ret = []
        ma_period = 20
        vol_period = 20
        sigma_level = 2
        def fun():  # noqa : E306
            nonlocal ret
            ret = get_upper_bollinger_band(np_data, ma_period, vol_period, sigma_level)

        measure_runtime(100, fun)
        self.assertIsInstance(ret, np.ndarray)

    def test_lower_bolliger_band_is_valid(self):
        data = get_test_data()

        ma_period = 25
        vol_period = 20
        sigma_level = 2
        calcaulated_by_indicator = np.zeros(shape=(len(data) - max(ma_period - 1, vol_period - 1), len(data.columns)))

        def get_indicator(data, ma_period, vol_period, sigma_level):  # noqa : E306
            return BollingerBand(data, ma_period, vol_period, sigma_level)

        func = partial(get_indicator, ma_period=ma_period, vol_period=vol_period, sigma_level=sigma_level)
        indicator_name = 'LBAND'
        get_result_from_indicator(data, calcaulated_by_indicator, func, indicator_name)

        np_data = data.values
        np_calculated = get_lower_bollinger_band(np_data, ma_period, vol_period, sigma_level)

        self.assertTrue(np.isclose(calcaulated_by_indicator, np_calculated, atol=10e-13).sum() == np_calculated.size)

    def test_lower_bollinger_band_runtime(self):
        data = get_test_data()
        np_data = data.values

        ret = []
        ma_period = 20
        vol_period = 20
        sigma_level = 2
        def fun():  # noqa : E306
            nonlocal ret
            ret = get_lower_bollinger_band(np_data, ma_period, vol_period, sigma_level)

        measure_runtime(100, fun)
        self.assertIsInstance(ret, np.ndarray)

    def test_percent_b_is_valid(self):
        data = get_test_data()

        ma_period = 25
        vol_period = 20
        sigma_level = 2
        calcaulated_by_indicator = np.zeros(shape=(len(data) - max(ma_period - 1, vol_period - 1), len(data.columns)))

        def get_indicator(data, ma_period, vol_period, sigma_level):  # noqa : E306
            return PercentB(data, ma_period, vol_period, sigma_level)

        func = partial(get_indicator, ma_period=ma_period, vol_period=vol_period, sigma_level=sigma_level)
        indicator_name = '%B'
        get_result_from_indicator(data, calcaulated_by_indicator, func, indicator_name)

        np_data = data.values
        np_calculated = get_percent_b(np_data, ma_period, vol_period, sigma_level)

        self.assertTrue(np.isclose(calcaulated_by_indicator, np_calculated, atol=10e-13).sum() == np_calculated.size)

    def test_percent_b_runtime(self):
        data = get_test_data()
        np_data = data.values

        ret = []
        ma_period = 20
        vol_period = 20
        sigma_level = 2
        def fun():  # noqa : E306
            nonlocal ret
            ret = get_percent_b(np_data, ma_period, vol_period, sigma_level)

        measure_runtime(100, fun)
        self.assertIsInstance(ret, np.ndarray)

    def test_bandwidth_is_valid(self):
        data = get_test_data()

        ma_period = 25
        vol_period = 20
        sigma_level = 2
        calcaulated_by_indicator = np.zeros(shape=(len(data) - max(ma_period - 1, vol_period - 1), len(data.columns)))

        def get_indicator(data, ma_period, vol_period, sigma_level):  # noqa : E306
            return BandWidth(data, ma_period, vol_period, sigma_level)

        func = partial(get_indicator, ma_period=ma_period, vol_period=vol_period, sigma_level=sigma_level)
        indicator_name = 'BANDWIDTH'
        get_result_from_indicator(data, calcaulated_by_indicator, func, indicator_name)

        np_data = data.values
        np_calculated = get_bandwidth(np_data, ma_period, vol_period, sigma_level)

        self.assertTrue(np.isclose(calcaulated_by_indicator, np_calculated, atol=10e-13).sum() == np_calculated.size)

    def test_bandwidth_runtime(self):
        data = get_test_data()
        np_data = data.values

        ret = []
        ma_period = 20
        vol_period = 20
        sigma_level = 2
        def fun():  # noqa : E306
            nonlocal ret
            ret = get_bandwidth(np_data, ma_period, vol_period, sigma_level)

        measure_runtime(100, fun)
        self.assertIsInstance(ret, np.ndarray)

    def test_rsi_is_valid(self):
        data = get_test_data()

        period = 14
        calcaulated_by_indicator = np.zeros(shape=(len(data) - period, len(data.columns)))

        def get_indicator(data, period):  # noqa : E306
            return RSI(data, period)

        func = partial(get_indicator, period=period)
        indicator_name = 'RSI'
        get_result_from_indicator(data, calcaulated_by_indicator, func, indicator_name)

        np_data = data.values
        np_calculated = get_rsi(np_data, period)

        self.assertTrue(np.isclose(calcaulated_by_indicator, np_calculated, atol=10e-13).sum() == np_calculated.size)

    def test_rsi_runtime(self):
        data = get_test_data()
        np_data = data.values

        ret = []
        period = 20
        def fun():  # noqa : E306
            nonlocal ret
            ret = get_rsi(np_data, period)

        measure_runtime(100, fun)
        self.assertIsInstance(ret, np.ndarray)

    def test_rolling_max_runtime(self):
        data = get_test_data()
        np_data = data.values

        period = 20

        calculated_by_numpy = np.zeros_like(data)
        for i in range(len(data.columns)):
            calculated_by_numpy[:, i] = data.rolling(period).max().iloc[:, i]

        calculated_by_numpy = calculated_by_numpy[period - 1:, :]
        np_calculated = get_rolling_max(np_data, period)

        self.assertTrue(np.isclose(calculated_by_numpy, np_calculated, atol=10e-13).sum() == np_calculated.size)

    def test_rolling_min_runtime(self):
        data = get_test_data()
        np_data = data.values

        period = 20

        calculated_by_numpy = np.zeros_like(data)
        for i in range(len(data.columns)):
            calculated_by_numpy[:, i] = data.rolling(period).min().iloc[:, i]

        calculated_by_numpy = calculated_by_numpy[period - 1:, :]
        np_calculated = get_rolling_min(np_data, period)

        self.assertTrue(np.isclose(calculated_by_numpy, np_calculated, atol=10e-13).sum() == np_calculated.size)


def measure_runtime(num_of_iteration, something):
    global_time = 0
    for i in range(num_of_iteration):
        start_time = time()
        something()
        end_time = time()
        global_time += end_time - start_time
    print('mean time: ' + str(global_time / num_of_iteration))


def get_result_from_indicator(data, np_array, indicator_allocation, indicator_name):
    count = 0
    for ticker in data.columns:
        indicator = indicator_allocation(data[[ticker]])
        indicator.calculate()
        np_array[:, count] = indicator.get_indicator()[indicator_name].dropna().values
        count += 1


if __name__ == '__main__':
    unittest.main()
