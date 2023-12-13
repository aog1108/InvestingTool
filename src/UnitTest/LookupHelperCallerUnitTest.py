import unittest
import sys

sys.path.append('C:/Users/JeonSeongHun/PycharmProjects/InvestingTool')


if True:  # noqa: E402
    from LookupHelperCaller import *
    from TestData import get_test_data
    import numpy as np


class LookupHelperCallerTestCase(unittest.TestCase):
    def test_return_is_valid(self):
        data = get_test_data()

        np_data = np.array(data)
        period = 3
        input_json = {'period': period}

        lookup_helper_caller = lookup_helper_caller_factory('return', input_json)

        ret1 = get_return(np_data, period)
        ret2 = lookup_helper_caller.call_lookup_helper_function(np_data)

        self.assertTrue(np.isclose(ret1 - ret2, 0, atol=10e-13).sum() == ret1.size)

    def test_volatility_is_valid(self):
        data = get_test_data()

        np_data = np.array(data)
        period = 3
        input_json = {'period': period}

        lookup_helper_caller = lookup_helper_caller_factory('volatility', input_json)

        ret1 = get_volatility(np_data, period)
        ret2 = lookup_helper_caller.call_lookup_helper_function(np_data)

        self.assertTrue(np.isclose(ret1 - ret2, 0, atol=10e-13).sum() == ret1.size)

    def test_std_is_valid(self):
        data = get_test_data()

        np_data = np.array(data)
        period = 10
        input_json = {'period': period}

        lookup_helper_caller = lookup_helper_caller_factory('standard_deviation', input_json)

        ret1 = get_standard_deviation(np_data, period)
        ret2 = lookup_helper_caller.call_lookup_helper_function(np_data)

        self.assertTrue(np.isclose(ret1 - ret2, 0, atol=10e-13).sum() == ret1.size)

    def test_sma_is_valid(self):
        data = get_test_data()

        np_data = np.array(data)
        period = 10
        input_json = {'period': period}

        lookup_helper_caller = lookup_helper_caller_factory('simple_moving_average', input_json)

        ret1 = get_simple_moving_average(np_data, period)
        ret2 = lookup_helper_caller.call_lookup_helper_function(np_data)

        self.assertTrue(np.isclose(ret1 - ret2, 0, atol=10e-13).sum() == ret1.size)

    def test_ema_is_valid(self):
        data = get_test_data()

        np_data = np.array(data)
        period = 10
        input_json = {'period': period}

        lookup_helper_caller = lookup_helper_caller_factory('exponential_moving_average', input_json)

        ret1 = get_exponential_moving_average(np_data, period)
        ret2 = lookup_helper_caller.call_lookup_helper_function(np_data)

        self.assertTrue(np.isclose(ret1 - ret2, 0, atol=10e-13).sum() == ret1.size)

    def test_ub_is_valid(self):
        data = get_test_data()

        np_data = np.array(data)
        ma_period = 20
        std_period = 20
        sigma_level = 2
        input_json = {'ma_period': ma_period,
                      'std_period': std_period,
                      'sigma_level': sigma_level}

        lookup_helper_caller = lookup_helper_caller_factory('upper_bollinger_band', input_json)

        ret1 = get_upper_bollinger_band(np_data, ma_period, std_period, sigma_level)
        ret2 = lookup_helper_caller.call_lookup_helper_function(np_data)

        self.assertTrue(np.isclose(ret1 - ret2, 0, atol=10e-13).sum() == ret1.size)

    def test_lb_is_valid(self):
        data = get_test_data()

        np_data = np.array(data)
        ma_period = 20
        std_period = 20
        sigma_level = 2
        input_json = {'ma_period': ma_period,
                      'std_period': std_period,
                      'sigma_level': sigma_level}

        lookup_helper_caller = lookup_helper_caller_factory('lower_bollinger_band', input_json)

        ret1 = get_lower_bollinger_band(np_data, ma_period, std_period, sigma_level)
        ret2 = lookup_helper_caller.call_lookup_helper_function(np_data)

        self.assertTrue(np.isclose(ret1 - ret2, 0, atol=10e-13).sum() == ret1.size)

    def test_percent_b_is_valid(self):
        data = get_test_data()

        np_data = np.array(data)
        ma_period = 20
        std_period = 20
        sigma_level = 2
        input_json = {'ma_period': ma_period,
                      'std_period': std_period,
                      'sigma_level': sigma_level}

        lookup_helper_caller = lookup_helper_caller_factory('percent_b', input_json)

        ret1 = get_percent_b(np_data, ma_period, std_period, sigma_level)
        ret2 = lookup_helper_caller.call_lookup_helper_function(np_data)

        self.assertTrue(np.isclose(ret1 - ret2, 0, atol=10e-13).sum() == ret1.size)

    def test_bandwidth_is_valid(self):
        data = get_test_data()

        np_data = np.array(data)
        ma_period = 20
        std_period = 20
        sigma_level = 2
        input_json = {'ma_period': ma_period,
                      'std_period': std_period,
                      'sigma_level': sigma_level}

        lookup_helper_caller = lookup_helper_caller_factory('bandwidth', input_json)

        ret1 = get_bandwidth(np_data, ma_period, std_period, sigma_level)
        ret2 = lookup_helper_caller.call_lookup_helper_function(np_data)

        self.assertTrue(np.isclose(ret1 - ret2, 0, atol=10e-13).sum() == ret1.size)

    def test_rsi_is_valid(self):
        data = get_test_data()

        np_data = np.array(data)
        period = 14
        input_json = {'period': period}

        lookup_helper_caller = lookup_helper_caller_factory('rsi', input_json)

        ret1 = get_rsi(np_data, period)
        ret2 = lookup_helper_caller.call_lookup_helper_function(np_data)

        self.assertTrue(np.isclose(ret1 - ret2, 0, atol=10e-13).sum() == ret1.size)


if __name__ == '__main__':
    unittest.main()
