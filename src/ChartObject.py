import matplotlib.pyplot as plt
import pandas as pd
from copy import deepcopy
from TechnicalIndicatorHelper import data_type_check


class ChartObject:
    def __init__(self, data):
        data_type_check(data)
        self.__data = data
        self.__indicators = []
        self.__names = []

    def register_indicator(self, indicator):
        self.__indicators.append(indicator)
        self.__names.append(indicator.get_name())

    def calculate(self):
        for indicator in self.__indicators:
            indicator.calculate()

    def get_indicator_by_index(self, index):
        return deepcopy(self.__indicators[index])

    def get_indicator_by_name(self, name):
        index = self.__names.index(name)
        return deepcopy(self.__indicators[index])

    def get_concatenated_indicators(self):
        concatenated_indicators = pd.concat(list(map(lambda x: x.get_indicator(), self.__indicators)), axis=1)
        return concatenated_indicators

    def plot(self, *args):
        start_date = pd.to_datetime(args[0])
        end_date = pd.to_datetime(args[1])

        plt.plot(self.__data.loc[start_date:end_date])
        for indicator in self.__indicators:
            plt.plot(indicator.get_indicator().loc[start_date:end_date])
        plt.xticks(rotation=45)
        plt.show()

