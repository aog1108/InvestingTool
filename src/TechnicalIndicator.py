from abc import *
from TechnicalIndicatorHelper import *


class TechnicalIndicator:
    """
    Base class for technical indicators

    data : Raw data(It must be the DataFrame Type)
    indicator : Calculated indicator(calculated by calculate method)
    name : The name of indicator(to be initialized in derived classes)
    """
    def __init__(self, data):
        data_type_check(data)
        data_column_len_check(data)
        self._data = data
        self._indicator = pd.DataFrame()
        self._name = ''

    @abstractmethod
    def calculate(self):
        pass

    def get_name(self):
        return self._name

    def get_indicator(self):
        return self._indicator

    def get_columns(self):
        return self._indicator.columns

    def get_index(self):
        return self._indicator.index

    def get_values(self):
        return self._indicator.values


class Return(TechnicalIndicator):
    """
    Return Class

    period : the number of days of return

    Columns: RETURN + period
    RETURN : Non-annualized period-day return
    """
    def __init__(self, data, period=1):
        super(Return, self).__init__(data)
        self._name = 'Return'
        self.__period = period

    def calculate(self):
        self._indicator = (self._data - self._data.shift(1)) / self._data.shift(1)
        self._indicator.columns = ['RETURN ' + str(self.__period)]


class Volatility(TechnicalIndicator):
    """
    Volatility Class

    period : the number of days of return

    Columns: VOLATILITY + period
    VOLATILITY : annualized volatility
    """
    def __init__(self, data, period):
        super(Volatility, self).__init__(data)
        self._name = 'Volatility'
        self.__period = period

    def calculate(self):
        ret = Return(self._data, 1)
        ret.calculate()
        ret = ret.get_indicator()
        self._indicator = np.sqrt(252) * ret.rolling(self.__period).std()
        self._indicator.columns = ['VOLATILITY ' + str(self.__period)]


class MovingAverage(TechnicalIndicator):
    """
    Moving average class

    ma_type
    0 : Simple, 1: Exponential, 2: Weighted

    Columns: MA + ma_period
    MA : Moving average, period = ma_period
    """
    def __init__(self, data, ma_period, ma_type):
        super(MovingAverage, self).__init__(data)
        self._name = 'Moving Average'
        self.__ma_period = ma_period
        self.__ma_type = ma_type

        if self.__ma_type == 0:
            self.__calculate_impl = simple_moving_average
        elif self.__ma_type == 1:
            self.__calculate_impl = exponential_moving_average
        elif self.__ma_type == 2:
            self.__calculate_impl = weighted_moving_average

    def calculate(self):
        self._indicator = self.__calculate_impl(self._data, self.__ma_period)
        self._indicator.columns = ['MA ' + str(self.__ma_period)]


class BollingerBand(TechnicalIndicator):
    """
    Bollinger Band Class

    ma_type
    0 : Simple, 1: Exponential, 2: Weighted

    Columns: UBAND / LBAND
    UBAND : Moving average + sigma_level * Moving average volatility
    MBAND : Moving average
    LBAND : Moving average - sigma_level * Moving average volatility
    """
    def __init__(self, data, ma_period=20, vol_period=20, sigma_level=2, ma_type=0):
        super(BollingerBand, self).__init__(data)
        self._name = 'Bollinger Band'
        self.__ma_period = ma_period
        self.__vol_period = vol_period
        self.__sigma_level = sigma_level
        self.__ma_type = ma_type

    def calculate(self):
        ma = MovingAverage(self._data, self.__ma_period, self.__ma_type)
        ma.calculate()
        ma = ma.get_indicator()
        std = self._data.rolling(self.__vol_period).std()
        uband = np.array(ma) + np.array(self.__sigma_level * std)
        lband = np.array(ma) - np.array(self.__sigma_level * std)
        values = np.append(np.append(ma, uband, axis=1), lband, axis=1)
        self._indicator = pd.DataFrame(values, columns=['MBAND', 'UBAND', 'LBAND'], index=ma.index)


class PercentB(TechnicalIndicator):
    """
    Percent B Class

    ma_type
    0 : Simple, 1: Exponential, 2: Weighted

    Columns: %B
    %B : Bollinger Band %B
    """
    def __init__(self, data, ma_period=20, vol_period=20, sigma_level=2, ma_type=0):
        super(PercentB, self).__init__(data)
        self._name = '%B'
        self.__ma_period = ma_period
        self.__vol_period = vol_period
        self.__sigma_level = sigma_level
        self.__ma_type = ma_type

    def calculate(self):
        bb = BollingerBand(self._data, self.__ma_period, self.__vol_period, self.__sigma_level, self.__ma_type)
        bb.calculate()
        bb_data = bb.get_indicator()

        self._indicator = (np.array(self._data)
                           - np.array(bb_data[['LBAND']])) / (np.array(bb_data[['UBAND']])
                                                              - np.array(bb_data[['LBAND']]))
        self._indicator = pd.DataFrame(self._indicator, columns=['%B'], index=bb_data.index)


class BandWidth(TechnicalIndicator):
    """
    BandWidth Class

    ma_type
    0 : Simple, 1: Exponential, 2: Weighted

    Columns: BandWidth

    """
    def __init__(self, data, ma_period=20, vol_period=20, sigma_level=2, ma_type=0):
        super(BandWidth, self).__init__(data)
        self.__ma_period = ma_period
        self.__vol_period = vol_period
        self.__sigma_level = sigma_level
        self.__ma_type = ma_type

    def calculate(self):
        bb = BollingerBand(self._data, self.__ma_period, self.__vol_period, self.__sigma_level, self.__ma_type)
        bb.calculate()
        bb_data = bb.get_indicator()

        self._indicator = (np.array(bb_data['UBAND'])
                           - np.array(bb_data['LBAND'])) / np.array(bb_data['MBAND'])
        self._indicator = pd.DataFrame(self._indicator, columns=['BANDWIDTH'], index=bb_data.index)


class RSI(TechnicalIndicator):
    """
    RSI Class

    Columns: RSI
    RSI : RSI
    """
    def __init__(self, data, period=14):
        super(RSI, self).__init__(data)
        self._name = 'RSI'
        self.__period = period

    def calculate(self):
        diff = self._data.diff()
        u = np.maximum(diff, 0)
        d = np.maximum(-diff, 0)
        au = u.rolling(self.__period).mean()
        ad = d.rolling(self.__period).mean()
        rs = au / ad
        self._indicator = 100 - 100 / (1 + rs)
        self._indicator.columns = ['RSI']

