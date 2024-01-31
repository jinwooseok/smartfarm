import pandas as pd
import numpy as np
from .masks import *

class DailyFeatureGenerator():
    def __init__(self, data, var=None):
        self.data = data
        self.date_series = data['날짜']
        self.var = var
    
    def execute(self):
        return_list = []
        print(self.var)
        for variable in self.var:
            temp = list(variable.keys())[0]
            standards = variable[temp]
            for standard in standards:
                feature_df = DailyFeatureGenerator.generating_variable(self.data, self.date_series, temp, standard)
                return_list.append(feature_df)
        
        merged_df = return_list[0]
        for i in range(1, len(return_list)):
            merged_df = pd.merge(merged_df, return_list[i], on='날짜', how='left')
        return merged_df
    
    def generating_variable(data, date_series, temp,standard, t_diff=2, div_DN=False, tbase=15): 
        
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
        
        timing_key = standard[0]
        #타이밍이 들어있는 열을 찾는다.
        if timing_key == '전체':
            timing_series = date_series
        else:
            timing_series = data[timing_dict[timing_key]]
        
        function_key = standard[1]
        function = functions_dict[function_key]
        
        period = 1
        
        temp_list = []
        date_list = []
        standard_date = date_series.iloc[0]
        last_date = date_series.iloc[-1]
        while last_date >= standard_date:
            total_mask = DailyFeatureGenerator.total_mask(date_series, standard_date, period, timing_series, timing_key)
            temp = DailyFeatureGenerator.daily_grouping(total_mask, data, target_column, function)
            temp_list.append(temp)
            date_list.append(standard_date)
            standard_date += pd.Timedelta(days=period)
        print(temp_list)
        return_df = pd.DataFrame({'날짜':date_list, f'{timing_key}{function_key}{target_column}':temp_list})
        return return_df
    
    def total_mask(date_series, standard_date, period, timing_series, timing_key):
        daily_mask = daily_mask_generator(date_series, standard_date, period)
        if timing_key == '전체':
            timing_mask = daily_mask
        else:
            timing_mask = timing_mask_generator(timing_series, timing_key)
        return total_mask_generator([daily_mask, timing_mask])
    
    def daily_grouping(mask, data, target_column, function):
        if mask.sum() == 0:
            np.nan
        else:
            return function(data[target_column].loc[mask])
   
   
    def DIF(data):
        return max(data) - min(data)
   
    def GDD(data, tbase=15):
        temp = (max(data)+min(data))/2 - tbase
        if temp >= 0:
            return temp
        else:
            return 0
        
    def mean(data):
        if len(data) == 0:
            return np.nan
        else:
            return sum(data)/len(data)

    def min(data):
        if len(data) == 0:
            return np.nan
        else:
            return data.min()

    def max(data):
        if len(data) == 0:
            return np.nan
        else:
            return data.max()