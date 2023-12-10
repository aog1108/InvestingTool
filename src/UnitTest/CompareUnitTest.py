import unittest
import sys

sys.path.append('C:/Users/JeonSeongHun/PycharmProjects/TechnicalBacktesting')


if True:  # noqa: E402
    from LookupHelperCaller import *
    from Compare import *
    from TestData import *
    import numpy as np


class CompareUnitTest(unittest.TestCase):
    data = get_test_data_all()

    def test1(self):
        np_data = np.array(CompareUnitTest.data)

        ma_period = 20
        std_period = 20
        sigma_level = 2
        input_json = {'ma_period': ma_period,
                      'std_period': std_period,
                      'sigma_level': sigma_level}

        lookup_helper_caller = lookup_helper_caller_factory('upper_bollinger_band', input_json)

        upper_bollinger_band = lookup_helper_caller.call_lookup_helper_function(np_data)
        length = upper_bollinger_band.shape[0]
        shrinked_data = np_data[-length:, :]

        compare_method1 = LeftGreaterThanRight()
        compare_method2 = LeftLessThanRight()

        raw_compared_result1 = (shrinked_data - upper_bollinger_band > 0).sum(axis=0).astype(bool)
        raw_compared_result2 = (shrinked_data - 1.05 * upper_bollinger_band < 0).sum(axis=0).astype(bool)

        compared_result1 = compare_method1.compare(shrinked_data, upper_bollinger_band)
        compared_result2 = compare_method2.compare(shrinked_data, 1.05 * upper_bollinger_band)

        raw_compared_result = np.logical_and(raw_compared_result1, raw_compared_result2)
        compare_result = np.logical_and(compared_result1, compared_result2)

        self.assertTrue(np.equal(raw_compared_result, compare_result).sum() == len(compare_result))

    def test2(self):
        np_data = np.array(CompareUnitTest.data)

        ma_period = 20
        std_period = 20
        sigma_level = 2
        input_json = {'ma_period': ma_period,
                      'std_period': std_period,
                      'sigma_level': sigma_level}

        lookup_helper_caller1 = lookup_helper_caller_factory('bandwidth', input_json)
        lookup_helper_caller2 = lookup_helper_caller_factory('lower_bollinger_band', input_json)

        bandwidth = lookup_helper_caller1.call_lookup_helper_function(np_data)
        lower_bollinger_band = lookup_helper_caller2.call_lookup_helper_function(np_data)

        data_json = {'price': np_data,
                     'bandwidth': bandwidth,
                     'lower_bollinger_band': lower_bollinger_band}

        preprocessing_data_as_shortest_data_length(data_json)

        compare_method1 = LeftLessThanRight()
        compare_method2 = LeftGreaterThanRight()

        raw_compared_result1 = (data_json['bandwidth'] < 0.3).sum(axis=0).astype(bool)
        raw_compared_result2 = ((data_json['price'] - data_json['lower_bollinger_band'])
                                / data_json['price'] > 0).sum(axis=0).astype(bool)
        raw_compared_result3 = ((data_json['price'] - data_json['lower_bollinger_band'])
                                / data_json['price'] < 0.01).sum(axis=0).astype(bool)

        compared_result1 = compare_method1.compare(data_json['bandwidth'], 0.3)
        compared_result2 = compare_method2.compare((data_json['price'] - data_json['lower_bollinger_band'])
                                                   / data_json['price'], 0)
        compared_result3 = compare_method1.compare((data_json['price'] - data_json['lower_bollinger_band'])
                                                   / data_json['price'], 0.01)

        raw_compared_result = satisfy_all_condition(raw_compared_result1, raw_compared_result2, raw_compared_result3)
        compare_result = satisfy_all_condition(compared_result1, compared_result2, compared_result3)

        self.assertTrue(np.equal(raw_compared_result, compare_result).sum() == len(compare_result))

    def test3(self):
        np_data = np.array(CompareUnitTest.data)

        ma_period = 20
        std_period = 20
        sigma_level = 2
        input_json = {'ma_period': ma_period,
                      'std_period': std_period,
                      'sigma_level': sigma_level}

        lookup_helper_caller1 = lookup_helper_caller_factory('bandwidth', input_json)
        lookup_helper_caller2 = lookup_helper_caller_factory('lower_bollinger_band', input_json)

        bandwidth = lookup_helper_caller1.call_lookup_helper_function(np_data)
        lower_bollinger_band = lookup_helper_caller2.call_lookup_helper_function(np_data)

        data_json = {'price': np_data,
                     'bandwidth': bandwidth,
                     'lower_bollinger_band': lower_bollinger_band}

        preprocessing_data_as_shortest_data_length(data_json)

        period = 3

        compare_method1 = LeftLessThanRight('AtLeast', period)
        compare_method2 = LeftGreaterThanRight('AtLeast', period)

        raw_compared_result1 = (data_json['bandwidth'] < 0.3)[-period:, :].sum(axis=0).astype(bool)
        raw_compared_result2 = ((data_json['price'] - data_json['lower_bollinger_band'])
                                / data_json['price'] > 0)[-period:, :].sum(axis=0).astype(bool)
        raw_compared_result3 = ((data_json['price'] - data_json['lower_bollinger_band'])
                                / data_json['price'] < 0.01)[-period:, :].sum(axis=0).astype(bool)

        compared_result1 = compare_method1.compare(data_json['bandwidth'], 0.3)
        compared_result2 = compare_method2.compare((data_json['price'] - data_json['lower_bollinger_band'])
                                                   / data_json['price'], 0)
        compared_result3 = compare_method1.compare((data_json['price'] - data_json['lower_bollinger_band'])
                                                   / data_json['price'], 0.01)

        raw_compared_result = satisfy_all_condition(raw_compared_result1, raw_compared_result2, raw_compared_result3)
        compare_result = satisfy_all_condition(compared_result1, compared_result2, compared_result3)

        self.assertTrue(np.equal(raw_compared_result, compare_result).sum() == len(compare_result))

    def test4(self):
        np_data = np.array(CompareUnitTest.data)

        ma_period = 20
        std_period = 20
        sigma_level = 2
        input_json = {'ma_period': ma_period,
                      'std_period': std_period,
                      'sigma_level': sigma_level}

        lookup_helper_caller1 = lookup_helper_caller_factory('bandwidth', input_json)
        lookup_helper_caller2 = lookup_helper_caller_factory('lower_bollinger_band', input_json)

        bandwidth = lookup_helper_caller1.call_lookup_helper_function(np_data)
        lower_bollinger_band = lookup_helper_caller2.call_lookup_helper_function(np_data)

        data_json = {'price': np_data,
                     'bandwidth': bandwidth,
                     'lower_bollinger_band': lower_bollinger_band}

        preprocessing_data_as_shortest_data_length(data_json)

        period = 3

        compare_method1 = LeftLessThanRight('All', period)
        compare_method2 = LeftGreaterThanRight('All', period)

        raw_compared_result1 = ((data_json['bandwidth'] < 0.3)[-period:, :].sum(axis=0) == period).astype(bool)
        raw_compared_result2 = (((data_json['price'] - data_json['lower_bollinger_band'])
                                / data_json['price'] > 0)[-period:, :].sum(axis=0) == period).astype(bool)
        raw_compared_result3 = (((data_json['price'] - data_json['lower_bollinger_band'])
                                / data_json['price'] < 0.01)[-period:, :].sum(axis=0) == period).astype(bool)

        compared_result1 = compare_method1.compare(data_json['bandwidth'], 0.3)
        compared_result2 = compare_method2.compare((data_json['price'] - data_json['lower_bollinger_band'])
                                                   / data_json['price'], 0)
        compared_result3 = compare_method1.compare((data_json['price'] - data_json['lower_bollinger_band'])
                                                   / data_json['price'], 0.01)

        raw_compared_result = satisfy_all_condition(raw_compared_result1, raw_compared_result2, raw_compared_result3)
        compare_result = satisfy_all_condition(compared_result1, compared_result2, compared_result3)

        self.assertTrue(np.equal(raw_compared_result, compare_result).sum() == len(compare_result))


if __name__ == '__main__':
    unittest.main()
