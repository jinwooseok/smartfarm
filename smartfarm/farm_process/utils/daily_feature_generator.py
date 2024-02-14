import pandas as pd
import numpy as np
from .masks import *
from ..exceptions.exceptions import VarDataException
from ...file_data.utils.process import DataProcess
class DailyFeatureGenerator():
    def __init__(self, data, var=None):
        self.data = data
        self.date_series = data['날짜']
        self.var = var
    
    def execute(self):
        return_list = []
        timing_dict = {
            '전체' : '날짜',
            '주간' : 'day_night',
            '야간' : 'day_night',
            '일출부터정오' : 'srise_to_noon',
            f'일출전후2시간' : 'srise_diff'
        }
        #입력받았을 때 호출할 함수
        functions_dict = {
            '최소' : DailyFeatureGenerator.min,
            '최대' : DailyFeatureGenerator.max,
            '평균' : DailyFeatureGenerator.mean,
            '누적' : DailyFeatureGenerator.sum,
            'DIF' : DailyFeatureGenerator.DIF,
            'GDD' : DailyFeatureGenerator.GDD,
            '온도차' : DailyFeatureGenerator.sub
        }
        data=self.data
        return_list = []
        for variable in self.var:
            try:
                temp = list(variable.keys())[0]
                standards = variable[temp]
            except:
                raise VarDataException(variable)
            for standard in standards:
                timing_key, function_key = standard
                function = functions_dict[function_key]
                data[temp] = DataProcess.to_numeric_or_none(data[temp])
                target_data = data[['날짜',temp]][(data[timing_dict[timing_key]]==timing_key)]
                if timing_key == '전체':
                    target_data = data[['날짜',temp]]
                grouped_df = target_data.groupby(pd.Grouper(key='날짜', freq='D')).agg({temp: function})
                print(grouped_df)
                new_name = f'{timing_key}{function_key}{temp}'
                grouped_df.rename(columns={temp:new_name}, inplace=True)
                return_list.append(grouped_df)
        return pd.concat(return_list, axis=1).reset_index()
    
    #def generating_variable(self, data, temp, standard, t_diff=2, div_DN=False, tbase=15): 
    def DIF(data):
        if len(data) == 0:
            return np.nan
        return max(data) - min(data)
   
    def GDD(data, tbase=15):
        if len(data) == 0:
            return np.nan
        temp = (max(data)+min(data))/2 - tbase
        if temp >= 0:
            return temp
        else:
            return 0
    def sub(data):
        if len(data) == 0:
            return np.nan
        else:
            return max(data) - min(data)
        
    def sum(data):
        if len(data) == 0:
            return np.nan
        else:
            return sum(data)
        
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