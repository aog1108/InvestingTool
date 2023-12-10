import unittest
import sys

sys.path.append('C:/Users/JeonSeongHun/PycharmProjects/TechnicalBacktesting')

if True:  # noqa: E402
    from DataRetriever import *
    import DBHandling as Db


class DataRetrieverTestCase(unittest.TestCase):
    def test_krx_stock_data_retrieve_all(self):
        db_info = Db.FinancialDBInfo()
        db_object = Db.DBObject(db_info)

        data_retriever = DataRetriever(db_object)
        start_date = '2023-08-10'
        end_date = '2023-08-11'

        data = data_retriever.krx_stock_data_retrieve(start_date, end_date)

        data.to_csv('Unit_test_krx_stock_data_retrieve_all.csv')
        db_object.close()
        self.assertIsInstance(data, pd.DataFrame)

    def test_krx_stock_data_retrieve_certain_tickers(self):
        db_info = Db.FinancialDBInfo()
        db_object = Db.DBObject(db_info)

        data_retriever = DataRetriever(db_object)
        start_date = '2023-08-10'
        end_date = '2023-08-11'

        data = data_retriever.krx_stock_data_retrieve(start_date, end_date, '*', ['005930', '002800', '003530'])

        data.to_csv('Unit_test_krx_stock_data_retrieve_certain_tickers.csv')
        db_object.close()
        self.assertIsInstance(data, pd.DataFrame)

    def test_krx_stock_data_retrieve_certain_tickers_and_columns(self):
        db_info = Db.FinancialDBInfo()
        db_object = Db.DBObject(db_info)

        data_retriever = DataRetriever(db_object)
        start_date = '2023-08-10'
        end_date = '2023-08-11'

        data = data_retriever.krx_stock_data_retrieve(start_date, end_date,
                                                      ['TICKER', 'DATE', 'OPEN', 'HIGH', 'LOW', 'CLOSE'],
                                                      ['005930', '002800', '003530'])

        data.to_csv('Unit_test_krx_stock_data_retrieve_certain_tickers_and_columns.csv')
        db_object.close()
        self.assertIsInstance(data, pd.DataFrame)


if __name__ == '__main__':
    unittest.main()
