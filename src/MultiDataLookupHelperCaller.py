from abc import *
from MultiDataLookupHelper import *


def multi_data_lookup_helper_caller_factory(indicator_name, input_json):
    if indicator_name == 'accumulation_candle':
        return AccumulationCandleLookupHelperCaller(input_json['high-low(%)'] / 100,
                                                          input_json['volume_return(%)'] / 100)


class MultiDataLookupHelperCaller:
    @abstractmethod
    def call_lookup_helper_function(self, *args):
        pass

    @abstractmethod
    def minimum_data_num_needed(self):
        pass


class AccumulationCandleLookupHelperCaller(MultiDataLookupHelperCaller):
    def __init__(self, high_low_cutoff, volume_return_cutoff):
        self.__high_low_cutoff = high_low_cutoff
        self.__volume_return_cutoff = volume_return_cutoff

    def call_lookup_helper_function(self, *args):
        return get_accumulation_candle(args[0], args[1], args[2],
                                              self.__high_low_cutoff,
                                              self.__volume_return_cutoff)

    def minimum_data_num_needed(self):
        return 2
