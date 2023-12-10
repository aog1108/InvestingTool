import pandas as pd


class TableList:
    krx_stock_data_table = 'KRX_STOCK_DATA'
    krx_listed_stock_info_table = 'KRX_LISTED_STOCKS_INFO'
    krx_delisted_stock_info_table = 'KRX_DELISTED_STOCKS_INFO'
    equity_index_data_table = 'EQUITY_INDEX_DATA'

    date_column_name = 'DATE'
    ticker_column_name = 'TICKER'
    name_column_name = 'NAME'


class DataRetriever:
    def __init__(self, db_object):
        self.__db_object = db_object
        self.__table_list = TableList()

    def krx_stock_data_retrieve(self, start_date, end_date, columns='*', tickers='ALL'):
        query = 'SELECT '

        if columns != 'ALL':
            column_list = list_to_string_with_comma_split(columns)
        else:
            column_list = columns

        query += column_list
        query += ' FROM ' + self.__table_list.krx_stock_data_table

        query += ' WHERE ' + self.__table_list.date_column_name + ' >= ' + decorate_str_with_apostrophe(start_date)
        query += ' AND ' + self.__table_list.date_column_name + ' <= ' + decorate_str_with_apostrophe(end_date)

        if tickers != 'ALL':
            where_condition = ' AND ' + self.__table_list.ticker_column_name + ' IN ' \
                              + list_to_string_with_comma_split(tickers, True)
            query += where_condition

        data = self.__db_object.select(query)
        data = pd.DataFrame.from_records(data)
        data.sort_values([self.__table_list.date_column_name, self.__table_list.ticker_column_name], inplace=True)
        data.reset_index(inplace=True, drop=True)

        return data

    def krx_trading_date_retrieve(self, start_date, end_date):
        query = ' SELECT DISTINCT ' + self.__table_list.date_column_name
        query += ' FROM ' + self.__table_list.equity_index_data_table
        query += ' WHERE ' + self.__table_list.date_column_name + ' >= ' + decorate_str_with_apostrophe(start_date)
        query += ' AND ' + self.__table_list.date_column_name + ' <= ' + decorate_str_with_apostrophe(end_date)
        query += ' AND ' + self.__table_list.ticker_column_name + ' = ' + decorate_str_with_apostrophe('KOSPI')

        data = self.__db_object.select(query)
        data = pd.DataFrame.from_records(data)

        return data

    def krx_stocks_full_list_retrieve(self):
        query = ' SELECT ' + self.__table_list.ticker_column_name + ', ' + self.__table_list.name_column_name
        query += ' FROM ' + self.__table_list.krx_listed_stock_info_table
        query += ' UNION '
        query += ' SELECT ' + self.__table_list.ticker_column_name + ', ' + self.__table_list.name_column_name
        query += ' FROM ' + self.__table_list.krx_delisted_stock_info_table

        data = self.__db_object.select(query)
        data = pd.DataFrame.from_records(data)

        return data


def decorate_str_with_apostrophe(string):
    return "'" + string + "'"


def list_to_string_with_comma_split(list_object, with_tuple=False):
    if with_tuple:
        ret = '('
    else:
        ret = ''

    for element in list_object:
        ret += str(element) + ', '

    if with_tuple:
        ret = ret[:-2] + ')'
    else:
        ret = ret[:-2]

    return ret
