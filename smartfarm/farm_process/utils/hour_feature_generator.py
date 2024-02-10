from .daily_feature_generator import DailyFeatureGenerator
from ..exceptions.exceptions import *
import pandas as pd
from .masks import *

class HourFeatureGenerator(DailyFeatureGenerator):
    def generating_variable(self, data, date_series, temp,standard, t_diff=2, div_DN=False, tbase=15): 
        timing_dict = {
            '전체' : 'all',
            '주간' : 'day_night',
            '야간' : 'day_night',
            '일출부터정오' : 'srise_to_noon',
            f'일출전후{t_diff}시간' : 'srise_diff'
        }
        
        #입력받았을 때 호출할 함수
        functions_dict = {
            '최소' : DailyFeatureGenerator.min,
            '최대' : DailyFeatureGenerator.max,
            '평균' : DailyFeatureGenerator.mean,
            '누적' : sum,
            'DIF' : DailyFeatureGenerator.DIF,
            'GDD' : DailyFeatureGenerator.GDD
        }
        target_column = temp
        
        try:
            timing_key = standard[0]
            #타이밍이 들어있는 열을 찾는다.
            if timing_key == '전체':
                timing_series = date_series
            else:
                timing_series = data[timing_dict[timing_key]]
            
            function_key = standard[1]
            function = functions_dict[function_key]
        except:
            raise VarDataException([temp, standard])
        
        period = 1
        
        temp_list = []
        date_list = []
        standard_date = date_series.iloc[0]
        last_date = date_series.iloc[-1]

        while last_date >= standard_date:
            total_mask = HourFeatureGenerator.total_mask(date_series, standard_date, period, timing_series, timing_key)
            temp = DailyFeatureGenerator.daily_grouping(total_mask, data, target_column, function)
            temp_list.append(temp)
            date_list.append(standard_date)
            standard_date += pd.Timedelta(hours=period)
        return_df = pd.DataFrame({'날짜':date_list, f'{timing_key}{function_key}{target_column}':temp_list})
        return return_df
    
    def total_mask(date_series, standard_date, period, timing_series, timing_key):
        daily_mask = daily_mask_generator(date_series, standard_date, period)
        hour_mask = hour_mask_generator(date_series, standard_date, period)
        if timing_key == '전체':
            timing_mask = daily_mask
        else:
            timing_mask = timing_mask_generator(timing_series, timing_key)
        return total_mask_generator([daily_mask, hour_mask, timing_mask])