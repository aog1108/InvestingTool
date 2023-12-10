from abc import *
import pandas as pd


class BitWrap:
    """
    Bitwise Wrapper
    This class is for wrapping just one signal handler so as to match method interface
    SignalHandler should be wrapped to use BitwiseHandler before trasfered as input

    Ex)
    1, 2, 3 : signal handler
    And(1, Or(2, 3)) : Error!
    And(BitWrap(1), Or(BitWrap(2), BitWrap(3)) : Proper!

    """
    def __init__(self, signal_handler):
        self.__signal_handler = signal_handler

    def do_bitwise_operation(self):
        return self.__signal_handler.produce_signal()


class BitwiseOperationHandler:
    """
    Bitwise Operation Handler

    args : List of bitwise wrappers
    """
    def __init__(self, *args):
        self._args = args
        self._results = pd.DataFrame()

    @abstractmethod
    def do_bitwise_operation(self):
        pass

    def _apply(self):
        results = list(map(lambda x: x.do_bitwise_operation(), self._args))
        self._results = pd.concat(results, axis=1)


class And(BitwiseOperationHandler):
    """
    And Condition

    args : List of bitwise wrappers
    """
    def __init__(self, *args):
        super(And, self).__init__(*args)

    def do_bitwise_operation(self):
        self._apply()
        signal = self._results.sum(axis=1)
        length = len(self._results.columns)
        signal = signal.apply(lambda x: x == length)
        signal.name = 'SIGNAL'
        signal = signal.astype(int)

        return signal


class Or(BitwiseOperationHandler):
    """
    Or Condition

    args : List of bitwise wrappers
    """
    def __init__(self, *args):
        super(Or, self).__init__(*args)

    def do_bitwise_operation(self):
        self._apply()
        signal = self._results.sum(axis=1)
        signal = signal.apply(lambda x: x >= 1)
        signal.name = 'SIGNAL'
        signal = signal.astype(int)

        return signal


class Not(BitwiseOperationHandler):
    """
    Not Condition

    args : List of bitwise wrappers
    """
    def __init__(self, *args):
        super(Not, self).__init__(*args)

    def do_bitwise_operation(self):
        self._apply()
        signal = self._results.sum(axis=1)
        signal = signal.apply(lambda x: x == 0)
        signal.name = 'SIGNAL'
        signal = signal.astype(int)

        return signal
