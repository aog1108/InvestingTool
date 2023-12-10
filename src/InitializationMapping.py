
# 필요한 데이터가 여러 개인 경우 List 변수로 표현하고 해당 순서가 Multi Data Lookup Helper Caller에 Input으로 전달하는 순서
needed_raw_data_mapping = {'volume_return': 'VOLUME',
                           'moving_average_volume': 'VOLUME',
                           'return': 'CLOSE',
                           'volatility': 'CLOSE',
                           'standard_deviation': 'CLOSE',
                           'simple_moving_average': 'CLOSE',
                           'exponential_moving_average': 'CLOSE',
                           'upper_bollinger_band': 'CLOSE',
                           'lower_bollinger_band': 'CLOSE',
                           'percent_b': 'CLOSE',
                           'bandwidth': 'CLOSE',
                           'rsi': 'CLOSE',
                           'accumulation_candle': ['HIGH', 'LOW', 'VOLUME'],
                           'rolling_max': 'CLOSE',
                           'rolling_min': 'CLOSE',
                           'max': 'CLOSE',
                           'min': 'CLOSE'}

