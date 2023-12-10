from abc import *
import numpy as np


class PeriodPrefix:
    def __init__(self, compare_period=1):
        self._compare_period = int(compare_period)

    @abstractmethod
    # compared result should be the result returned by Compare class(boolean numpy ndarray)
    def apply(self, compared_result):
        pass


class AtLeast(PeriodPrefix):
    def __init__(self, compare_period=1):
        super(AtLeast, self).__init__(compare_period)

    def apply(self, compared_result):
        sumed_result = compared_result.sum(axis=0)
        return sumed_result >= self._compare_period


def period_prefix_factory(prefix, compare_period):
    if prefix == 'AtLeast':
        return AtLeast(compare_period)


class Compare:
    def __init__(self, prefix, compare_period):
        self._period_prefix = period_prefix_factory(prefix, compare_period)
        self._compare_period = compare_period

    @abstractmethod
    # a should be equal size numpy ndarray
    # if b is numpy ndarray, then b should have equal size with a
    # in the case of numpy ndarray, row : time / column : stock
    def compare(self, a, b):
        pass


class LeftEqualToRight(Compare):
    def __init__(self, prefix='AtLeast', compare_period=1):
        super(LeftEqualToRight, self).__init__(prefix, compare_period)

    def compare(self, a, b):
        compared_result = np.equal(a, b)
        return self._period_prefix.apply(compared_result)


class LeftGreaterThanRight(Compare):
    def __init__(self, prefix='AtLeast', compare_period=1):
        super(LeftGreaterThanRight, self).__init__(prefix, compare_period)

    def compare(self, a, b):
        compared_result = np.greater(a, b)
        return self._period_prefix.apply(compared_result)


class LeftLessThanRight(Compare):
    def __init__(self, prefix='AtLeast', compare_period=1):
        super(LeftLessThanRight, self).__init__(prefix, compare_period)

    def compare(self, a, b):
        compared_result = np.less(a, b)
        return self._period_prefix.apply(compared_result)


class LeftNotMoreThanRight(Compare):
    def __init__(self, prefix='AtLeast', compare_period=1):
        super(LeftNotMoreThanRight, self).__init__(prefix, compare_period)

    def compare(self, a, b):
        compared_result = np.less_equal(a, b)
        return self._period_prefix.apply(compared_result)


class LeftNotLessThanRight(Compare):
    def __init__(self, prefix='AtLeast', compare_period=1):
        super(LeftNotLessThanRight, self).__init__(prefix, compare_period)

    def compare(self, a, b):
        compared_result = np.greater_equal(a, b)
        return self._period_prefix.apply(compared_result)


def compare_factory(compare, prefix, compare_period):
    if compare == '=':
        return LeftEqualToRight(prefix, compare_period)
    elif compare == '>=':
        return LeftNotLessThanRight(prefix, compare_period)
    elif compare == '>':
        return LeftGreaterThanRight(prefix, compare_period)
    elif compare == '<=':
        return LeftNotMoreThanRight(prefix, compare_period)
    elif compare == '<':
        return LeftLessThanRight(prefix, compare_period)


def satisfy_all_condition(*args):
    length = len(args)
    if length > 2:
        ret = np.logical_and(args[0], args[1])
        for data in args[2:]:
            ret = np.logical_and(ret, data)
        return ret
    elif length == 2:
        return np.logical_and(args[0], args[1])
    else:
        return args[0]


def preprocessing_data_as_shortest_data_length(data_json):
    data_length = []
    for key in data_json.keys():
        data_length.append(len(data_json[key]))

    minimun_data_length = min(data_length)

    for key in data_json.keys():
        data_json[key] = data_json[key][-minimun_data_length:, :]


