import DBHandling as Db
from DataRetriever import DataRetriever


def get_test_data():
    db_info = Db.FinancialDBInfo(Db.read_financial_db_info())
    db_object = Db.DBObject(db_info)
    data_retriever = DataRetriever(db_object)

    data = data_retriever.krx_stock_data_retrieve('2023-06-04', '2023-08-11',
                                                  ['TICKER', 'DATE', 'CLOSE'],
                                                  ['005930', '000120', '000140', '000660'])
    data = data.set_index(['TICKER', 'DATE'])
    data = data.stack().unstack(level=0)
    data = data.set_index(data.index.get_level_values(0))

    return data


def get_test_data_all():
    db_info = Db.FinancialDBInfo(Db.read_financial_db_info())
    db_object = Db.DBObject(db_info)
    data_retriever = DataRetriever(db_object)

    data = data_retriever.krx_stock_data_retrieve('2023-06-01', '2023-09-30',
                                                  ['TICKER', 'DATE', 'CLOSE'])

    data = data.set_index(['TICKER', 'DATE'])
    data = data.stack().unstack(level=0)
    data = data.set_index(data.index.get_level_values(0))

    return data
