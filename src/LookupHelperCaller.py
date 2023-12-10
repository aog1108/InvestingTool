from abc import *
from LookupHelper import *


def lookup_helper_caller_factory(indicator_name, input_json):
    if indicator_name == 'moving_average_volume':
        return SimpleMovingAverageLookupCaller(input_json['period'])
    elif indicator_name == 'return':
        return ReturnLookupCaller(input_json['period'])
    elif indicator_name == 'volatility':
        return VolatilityLookupCaller(input_json['period'])
    elif indicator_name == 'standard_deviation':
        return StandardDeviationLookupCaller(input_json['period'])
    elif indicator_name == 'simple_moving_average':
        return SimpleMovingAverageLookupCaller(input_json['period'])
    elif indicator_name == 'exponential_moving_average':
        return ExponentialMovingAverageLookupCaller(input_json['period'])
    elif indicator_name == 'upper_bollinger_band':
        return UpperBollingerBandLookupCaller(input_json['ma_period'],
                                              input_json['std_period'],
                                              input_json['sigma_level'])
    elif indicator_name == 'lower_bollinger_band':
        return LowerBollingerBandLookupCaller(input_json['ma_period'],
                                              input_json['std_period'],
                                              input_json['sigma_level'])
    elif indicator_name == 'percent_b':
        return PercentBLookupCaller(input_json['ma_period'], input_json['std_period'], input_json['sigma_level'])
    elif indicator_name == 'bandwidth':
        return BandWidthLookupCaller(input_json['ma_period'], input_json['std_period'], input_json['sigma_level'])
    elif indicator_name == 'rsi':
        return RSILookupCaller(input_json['period'])
    elif indicator_name == 'rolling_max':
        return RollingMaxLookupCaller(input_json['period'])
    elif indicator_name == 'rolling_min':
        return RollingMinLookupCaller(input_json['period'])
    elif indicator_name == 'max':
        return MaxLookupCaller(input_json['period'])
    elif indicator_name == 'min':
        return MinLookupCaller(input_json['period'])


class LookupHelperCaller:
    @abstractmethod
    def call_lookup_helper_function(self, data):
        pass

    @abstractmethod
    def minimum_data_num_needed(self):
        pass


class ReturnLookupCaller(LookupHelperCaller):
    def __init__(self, period):
        self.__period = period

    def call_lookup_helper_function(self, data):
        return get_return(data, self.__period)

    def minimum_data_num_needed(self):
        return self.__period


class VolatilityLookupCaller(LookupHelperCaller):
    def __init__(self, period):
        self.__period = period

    def call_lookup_helper_function(self, data):
        return get_volatility(data, self.__period)

    def minimum_data_num_needed(self):
        return self.__period + 1


class StandardDeviationLookupCaller(LookupHelperCaller):
    def __init__(self, period):
        self.__period = period

    def call_lookup_helper_function(self, data):
        return get_standard_deviation(data, self.__period)

    def minimum_data_num_needed(self):
        return self.__period


class SimpleMovingAverageLookupCaller(LookupHelperCaller):
    def __init__(self, period):
        self.__period = period

    def call_lookup_helper_function(self, data):
        return get_simple_moving_average(data, self.__period)

    def minimum_data_num_needed(self):
        return self.__period


class ExponentialMovingAverageLookupCaller(LookupHelperCaller):
    def __init__(self, period):
        self.__period = period

    def call_lookup_helper_function(self, data):
        return get_exponential_moving_average(data, self.__period)

    def minimum_data_num_needed(self):
        return self.__period


class UpperBollingerBandLookupCaller(LookupHelperCaller):
    def __init__(self, ma_period, std_period, sigma_level):
        self.__ma_period = ma_period
        self.__std_period = std_period
        self.__sigma_level = sigma_level

    def call_lookup_helper_function(self, data):
        return get_upper_bollinger_band(data, self.__ma_period, self.__std_period, self.__sigma_level)

    def minimum_data_num_needed(self):
        return max(self.__ma_period, self.__std_period)


class LowerBollingerBandLookupCaller(LookupHelperCaller):
    def __init__(self, ma_period, std_period, sigma_level):
        self.__ma_period = ma_period
        self.__std_period = std_period
        self.__sigma_level = sigma_level

    def call_lookup_helper_function(self, data):
        return get_lower_bollinger_band(data, self.__ma_period, self.__std_period, self.__sigma_level)

    def minimum_data_num_needed(self):
        return max(self.__ma_period, self.__std_period)


class PercentBLookupCaller(LookupHelperCaller):
    def __init__(self, ma_period, std_period, sigma_level):
        self.__ma_period = ma_period
        self.__std_period = std_period
        self.__sigma_level = sigma_level

    def call_lookup_helper_function(self, data):
        return get_percent_b(data, self.__ma_period, self.__std_period, self.__sigma_level)

    def minimum_data_num_needed(self):
        return max(self.__ma_period, self.__std_period)


class BandWidthLookupCaller(LookupHelperCaller):
    def __init__(self, ma_period, std_period, sigma_level):
        self.__ma_period = ma_period
        self.__std_period = std_period
        self.__sigma_level = sigma_level

    def call_lookup_helper_function(self, data):
        return get_bandwidth(data, self.__ma_period, self.__std_period, self.__sigma_level)

    def minimum_data_num_needed(self):
        return max(self.__ma_period, self.__std_period)


class RSILookupCaller(LookupHelperCaller):
    def __init__(self, period):
        self.__period = period

    def call_lookup_helper_function(self, data):
        return get_rsi(data, self.__period)

    def minimum_data_num_needed(self):
        return self.__period + 1


class RollingMaxLookupCaller(LookupHelperCaller):
    def __init__(self, period):
        self.__period = period

    def call_lookup_helper_function(self, data):
        return get_rolling_max(data, self.__period)

    def minimum_data_num_needed(self):
        return self.__period


class RollingMinLookupCaller(LookupHelperCaller):
    def __init__(self, period):
        self.__period = period

    def call_lookup_helper_function(self, data):
        return get_rolling_min(data, self.__period)

    def minimum_data_num_needed(self):
        return self.__period


class MaxLookupCaller(LookupHelperCaller):
    def __init__(self, period):
        self.__period = period

    def call_lookup_helper_function(self, data):
        return get_max(data)

    def minimum_data_num_needed(self):
        return self.__period


class MinLookupCaller(LookupHelperCaller):
    def __init__(self, period):
        self.__period = period

    def call_lookup_helper_function(self, data):
        return get_min(data)

    def minimum_data_num_needed(self):
        return self.__period


def minimum_data_num_needed(*args):
    minimum_data_nums = []
    for caller in args:
        minimum_data_nums.append(caller.minimum_data_num_needed())

    return min(minimum_data_nums)

