from ExcelIO import *
from DataRetriever import *
from LookupHelperCaller import *
from Compare import *
import xlwings as xw
import DBHandling as Db
from datetime import datetime
from copy import deepcopy
from CompareTextInterpreter import *
from InitializationMapping import *
from MultiDataLookupHelperCaller import *

wb = xw.Book('Stocks_Searcher.xlsm')
ws = wb.sheets('Searcher')
result_sheet = wb.sheets('Result')
db_object = Db.DBObject(Db.FinancialDBInfo(Db.read_financial_db_info()))
data_retriever = DataRetriever(db_object)

raw_data_list = ['open', 'high', 'low', 'close', 'volume']


def main():
    ret = get_search_result()

    result_sheet['Result'].expand('right').expand('down').clear_contents()
    result_sheet['Result'].options(pd.DataFrame, header=1, index=False, expand='Table').value = ret

    return 0


def get_search_date():
    return ws['Search_date'].value.strftime('%Y-%m-%d')


def is_simple_lookup_helper_caller_needed(needed_raw_data_names):
    if type(needed_raw_data_names) == str:
        return True
    else:
        return False


def generate_lookup_helper_caller_from_indicator_str(indicator_str, indicator_input_json_str):
    if indicator_str in raw_data_list:
        return None
    else:
        indicator_input_json = eval(indicator_input_json_str.replace('\n', ''))
        if is_simple_lookup_helper_caller_needed(needed_raw_data_mapping[indicator_str]):
            return lookup_helper_caller_factory(indicator_str, indicator_input_json)
        else:
            return multi_data_lookup_helper_caller_factory(indicator_str, indicator_input_json)


def convert_simple_filter_df(filter_df):
    json_list = []
    for index in filter_df.index:
        compare = compare_factory(filter_df.loc[index, 'Compare'], 'AtLeast', filter_df.loc[index, 'SatisfiedPeriod'])
        lookup_helper_caller = generate_lookup_helper_caller_from_indicator_str(filter_df.loc[index, 'Indicator'],
                                                                                filter_df.loc[index,
                                                                                              'IndicatorInputJson'])
        json = {'Sequence': filter_df.loc[index, 'Sequence'],
                'EntirePeriod': filter_df.loc[index, 'EntirePeriod'],
                'Compare': compare,
                'Indicator': filter_df.loc[index, 'Indicator'],
                'LookupHelperCaller': lookup_helper_caller,
                'Value': filter_df.loc[index, 'Value']}
        json_list.append(json)

    return json_list


def convert_compare_filter_df(filter_df):
    json_list = []
    for index in filter_df.index:
        compare = compare_factory(filter_df.loc[index, 'Compare'], 'AtLeast', filter_df.loc[index, 'SatisfiedPeriod'])
        lookup_helper_caller1 = generate_lookup_helper_caller_from_indicator_str(filter_df.loc[index, 'Indicator1'],
                                                                                 filter_df.loc[index,
                                                                                               'IndicatorInputJson1'])
        lookup_helper_caller2 = generate_lookup_helper_caller_from_indicator_str(filter_df.loc[index, 'Indicator2'],
                                                                                 filter_df.loc[index,
                                                                                               'IndicatorInputJson2'])

        json = {'Sequence': filter_df.loc[index, 'Sequence'],
                'EntirePeriod': filter_df.loc[index, 'EntirePeriod'],
                'Compare': compare,
                'Factor': filter_df.loc[index, 'Factor'],
                'Indicator1': filter_df.loc[index, 'Indicator1'],
                'Indicator2': filter_df.loc[index, 'Indicator2'],
                'LookupHelperCaller1': lookup_helper_caller1,
                'LookupHelperCaller2': lookup_helper_caller2}
        json_list.append(json)

    return json_list


def get_needed_period_from_filter_json(lookup_helper_caller, entire_period):
    if lookup_helper_caller is not None:
        return lookup_helper_caller.minimum_data_num_needed() + entire_period - 1
    else:
        return entire_period


def get_start_date_for_searching(search_date, simple_filter_jsons, compare_filter_jsons):
    needed_period_list = []
    for json in simple_filter_jsons:
        needed_period = get_needed_period_from_filter_json(json['LookupHelperCaller'], json['EntirePeriod'])
        needed_period_list.append(needed_period)

    for json in compare_filter_jsons:
        needed_period = get_needed_period_from_filter_json(json['LookupHelperCaller1'], json['EntirePeriod'])
        needed_period_list.append(needed_period)

        needed_period = get_needed_period_from_filter_json(json['LookupHelperCaller2'], json['EntirePeriod'])
        needed_period_list.append(needed_period)

    krx_trading_dates = data_retriever.krx_trading_date_retrieve('1990-01-01', search_date)
    krx_trading_dates = krx_trading_dates.sort_values('DATE', ascending=True)
    needed_data_num = int(max(needed_period_list))
    start_date = krx_trading_dates.iloc[-1 + 1 - needed_data_num, 0]

    return datetime.strftime(start_date, '%Y-%m-%d')


def get_data_for_searching(simple_filter_jsons, compare_filter_jsons):
    search_date = get_search_date()

    start_date = get_start_date_for_searching(search_date, simple_filter_jsons, compare_filter_jsons)

    data = data_retriever.krx_stock_data_retrieve(start_date, search_date)

    return data


def preprocess_data_for_certain_column(data, column_name):
    data = data[['TICKER', 'DATE', column_name]]
    data = data.set_index(['TICKER', 'DATE'])
    data = data.stack().unstack(level=0)
    data = data.set_index(data.index.get_level_values(0))

    return data


def get_preprocessed_data_json(data):
    ret = {}
    for col in data.columns:
        if col not in ['TICKER', 'DATE']:
            ret[col] = preprocess_data_for_certain_column(data, col)

    return ret


def get_indicator_result_from_filter_json(preprocessed_data_json, lookup_helper_caller, indicator_str, entire_period):
    if lookup_helper_caller is None:
        indicator = np.array(preprocessed_data_json[indicator_str.upper()])
    else:
        needed_raw_data_columns = needed_raw_data_mapping[indicator_str]
        if is_simple_lookup_helper_caller_needed(needed_raw_data_mapping[indicator_str]):
            processed_data = np.array(preprocessed_data_json[needed_raw_data_columns])
            indicator = lookup_helper_caller.call_lookup_helper_function(processed_data)
        else:
            processed_data_list = []
            for i in range(len(needed_raw_data_columns)):
                processed_data = np.array(preprocessed_data_json[needed_raw_data_columns[i]])
                processed_data_list.append(processed_data)

            indicator = lookup_helper_caller.call_lookup_helper_function(*processed_data_list)

    start_index = -int(entire_period)

    return indicator[start_index:, :]


def get_compare_boolean_arrayes(preprocessed_data_json, simple_filter_jsons, compare_filter_jsons):
    ret = {}
    for json in simple_filter_jsons:
        indicator = get_indicator_result_from_filter_json(preprocessed_data_json,
                                                          json['LookupHelperCaller'],
                                                          json['Indicator'],
                                                          json['EntirePeriod'])
        compare_result = json['Compare'].compare(indicator, json['Value'])
        ret[json['Sequence']] = compare_result

    for json in compare_filter_jsons:
        indicator1 = get_indicator_result_from_filter_json(preprocessed_data_json,
                                                           json['LookupHelperCaller1'],
                                                           json['Indicator1'],
                                                           json['EntirePeriod'])
        indicator2 = get_indicator_result_from_filter_json(preprocessed_data_json,
                                                           json['LookupHelperCaller2'],
                                                           json['Indicator2'],
                                                           json['EntirePeriod'])
        compare_result = json['Compare'].compare(indicator1, json['Factor'] * indicator2)
        ret[json['Sequence']] = compare_result

    return ret


def read_sequence_text():
    return ws['Sequence_condition'].value


def exist_start_with_certain_number(num, list_var):
    for var in list_var:
        if int(var[0]) == num:
            return True

    return False


def last_element_start_with_certain_number(num, list_var):
    elements = []
    for var in list_var:
        if int(var[0]) == num:
            elements.append(var)

    return elements[-1]


def parse_sequence_text(sequence_text):
    json = {}
    splited_text = sequence_text.split()

    global_depth = 0
    json[global_depth] = {0: []}
    for text in splited_text:
        if text == '(':
            global_depth += 1
            internal_depth = max(json[global_depth - 1].keys())
            json[global_depth - 1][internal_depth].append(global_depth)
            if global_depth not in json.keys():
                json[global_depth] = {0: []}
            else:
                internal_depth = max(json[global_depth].keys()) + 1
                json[global_depth][internal_depth] = []
        elif text == ')':
            global_depth -= 1
        else:
            internal_depth = max(json[global_depth].keys())
            json[global_depth][internal_depth].append(text)

    return json


def convert_parsed_sequence_to_expression(parsed_sequence, compared_boolean_json):
    # 가장 마지막 depth부터 역순환으로 Expression 생성
    reversed_keys = list(parsed_sequence.keys())[::-1]
    ret = deepcopy(parsed_sequence)
    max_key = max(reversed_keys)

    for key1 in reversed_keys:
        # 가장 마지막 depth 제외하고 이전 depth에서 생성된 Expression 객체를 올바른 자리에 덮어씌우는 과정
        if key1 != max_key:
            int_type_count = 0
            for key2 in parsed_sequence[key1].keys():
                for i in range(len(parsed_sequence[key1][key2])):
                    if type(ret[key1][key2][i]) == int:
                        ret[key1][key2][i] = ret[key1 + 1][int_type_count]
                        int_type_count += 1

        for key2 in parsed_sequence[key1].keys():
            internal_depth_list = ret[key1][key2]
            interpreter_list = []
            # alphabet condition 먼저 Expression 객체로 변환 후, 파싱된 sequence 객체 복사본에 덮어 씌움.
            for i in range(len(internal_depth_list)):
                if internal_depth_list[i] not in ['and', 'or', 'not']:
                    # 이전 depth에서 생성된 Expression 객체로 덮어 씌워져 있는 원소도 있으므로, str일 때만 Expression 객체로 변환
                    if type(internal_depth_list[i]) == str:
                        ret[key1][key2][i] = compare_interpreter_factory(internal_depth_list[i],
                                                                         compared_boolean_json[internal_depth_list[i]])

            # and, or, not 조건 Expression 객체로 변환
            for i in range(len(internal_depth_list)):
                if internal_depth_list[i] in ['and', 'or']:
                    # 다음 순서로 not인 오는 경우, not 다음 순서가 alphabet condition이므로 조건문 분기.
                    if internal_depth_list[i + 1] == 'not':
                        # not은 항상 먼저 Expression으로 변환해 줘야 함
                        not_interpreter = compare_interpreter_factory(internal_depth_list[i + 1],
                                                                      internal_depth_list[i + 2])
                        ret[key1][key2][i + 2] = not_interpreter
                        next_alphabet_condition_interpreter = not_interpreter
                    else:
                        next_alphabet_condition_interpreter = internal_depth_list[i + 1]

                    # 처음에는 앞 뒤 alphabet condition Expression 객체를 비교하는 Expression 객체 생성.
                    # 그 후엔 순차적으로 and/or 조건이 적용된 Expression 객체와 바로 뒤 alphabet condition Expression 비교 필요.
                    # 분기 처리 완료 시 최종적으로 한 internal depth의 Expression은 interpreter_list의 마지막 원소가 됨.
                    if len(interpreter_list) == 0:
                        expr = compare_interpreter_factory(internal_depth_list[i],
                                                           internal_depth_list[i - 1],
                                                           next_alphabet_condition_interpreter)
                        interpreter_list.append(expr)
                    else:
                        expr = compare_interpreter_factory(internal_depth_list[i],
                                                           interpreter_list[-1],
                                                           next_alphabet_condition_interpreter)
                        interpreter_list.append(expr)

                # 최종적으로 생성된 Expression 객체로 파싱된 sequence 복사본에 item을 덮어 씌움.
            ret[key1][key2] = interpreter_list[-1]

    return ret[0][0]


def get_compare_result():
    simple_filter_json = convert_simple_filter_df(read_table_as_dataframe(ws, 'SimpleFilter'))
    compare_filter_json = convert_compare_filter_df(read_table_as_dataframe(ws, 'CompareFilter'))
    data = get_data_for_searching(simple_filter_json, compare_filter_json)
    preprocessed_data_map = get_preprocessed_data_json(data)
    compare_results = get_compare_boolean_arrayes(preprocessed_data_map, simple_filter_json, compare_filter_json)
    sq_text = read_sequence_text()
    parsed_sequence = parse_sequence_text(sq_text)
    ret = convert_parsed_sequence_to_expression(parsed_sequence, compare_results)
    complete_result = ret.interpret()

    index = preprocessed_data_map['CLOSE'].columns

    return pd.Series(complete_result, index=index)


def get_search_result():
    ret = get_compare_result()
    stock_ticker_name = data_retriever.krx_stocks_full_list_retrieve()

    return stock_ticker_name[stock_ticker_name['TICKER'].isin(ret[ret].index)]
main()