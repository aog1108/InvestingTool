from abc import *
import numpy as np


def compare_interpreter_factory(expression_name, *args):
    if expression_name == 'and':
        return AndExpression(args[0], args[1])
    elif expression_name == 'or':
        return OrExpression(args[0], args[1])
    elif expression_name == 'not':
        return NotExpression(args[0])
    else:
        return TerminalExpression(args[0])


class Expression:
    @abstractmethod
    def interpret(self):
        pass


class TerminalExpression(Expression):
    def __init__(self, boolean_array):
        super(TerminalExpression, self).__init__()
        self.__boolean_array = boolean_array

    def interpret(self):
        return self.__boolean_array


class CompareExpression(Expression):
    def __init__(self, expression1, expression2):
        super(CompareExpression, self).__init__()
        self._expression1 = expression1
        self._expression2 = expression2

    @abstractmethod
    def interpret(self):
        pass


class AndExpression(CompareExpression):
    def __init__(self, expression1, expression2):
        super(AndExpression, self).__init__(expression1, expression2)

    def interpret(self):
        return np.logical_and(self._expression1.interpret(), self._expression2.interpret())


class OrExpression(CompareExpression):
    def __init__(self, expression1, expression2):
        super(OrExpression, self).__init__(expression1, expression2)

    def interpret(self):
        return np.logical_or(self._expression1.interpret(), self._expression2.interpret())


class NotExpression(Expression):
    def __init__(self, expression):
        super(NotExpression, self).__init__()
        self.__expression = expression

    def interpret(self):
        return np.logical_not(self.__expression.interpret())
