import unittest
import sys

sys.path.append('C:/Users/JeonSeongHun/PycharmProjects/InvestingTool')

if True:  # noqa: E402
    from Communication import *


class DataRetrieverTestCase(unittest.TestCase):
    def test1(self):
        simple_filter_json = convert_simple_filter_df(read_table_as_dataframe(ws, 'SimpleFilter'))
        compare_filter_json = convert_compare_filter_df(read_table_as_dataframe(ws, 'CompareFilter'))
        data = get_data_for_searching(simple_filter_json, compare_filter_json)
        compare_results = get_compare_boolean_arrayes(data, simple_filter_json, compare_filter_json)
        sq_text = read_sequence_text()
        parsed_sequence = parse_sequence_text(sq_text)
        ret = convert_parsed_sequence_to_expression(parsed_sequence, compare_results)
        complete_result = ret.interpret()

        raw_result = np.logical_and(compare_results['A'], compare_results['B'])
        raw_result = np.logical_and(raw_result, compare_results['C'])
        raw_result = np.logical_and(raw_result, compare_results['D'])
        raw_result = np.logical_and(raw_result, compare_results['E'])

        self.assertEqual(complete_result.sum(), raw_result.sum())

    def test2(self):
        simple_filter_json = convert_simple_filter_df(read_table_as_dataframe(ws, 'SimpleFilter'))
        compare_filter_json = convert_compare_filter_df(read_table_as_dataframe(ws, 'CompareFilter'))
        data = get_data_for_searching(simple_filter_json, compare_filter_json)
        compare_results = get_compare_boolean_arrayes(data, simple_filter_json, compare_filter_json)
        sq_text = read_sequence_text()
        parsed_sequence = parse_sequence_text(sq_text)
        ret = convert_parsed_sequence_to_expression(parsed_sequence, compare_results)
        complete_result = ret.interpret()

        raw_result = np.logical_or(compare_results['B'], compare_results['C'])
        raw_result = np.logical_and(raw_result, compare_results['D'])
        raw_result = np.logical_and(raw_result, compare_results['E'])
        raw_result = np.logical_not(raw_result)
        raw_result = np.logical_and(raw_result, compare_results['A'])

        self.assertEqual(complete_result.sum(), raw_result.sum())


if __name__ == '__main__':
    unittest.main()
