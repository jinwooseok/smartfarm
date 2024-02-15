import pandas as pd
import numpy as np
from .masks import *
from ..exceptions.exceptions import VarDataException
from ...file_data.utils.process import DataProcess
class FeatureGenerator():
    def __init__(self, data, interval, var=None):
        self.data = data
        self.date_series = data['날짜']
        self.var = var
        self.interval= interval
        self.timing_dict = {
            '전체' : '날짜',
            '주간' : 'day_night',
            '야간' : 'day_night',
            '일출부터정오' : 'srise_to_noon',
            f'일출전후2시간' : 'srise_diff'
        }
        self.functions_dict = {
            '최소' : self.min,
            '최대' : self.max,
            '평균' : self.mean,
            '누적' : self.sum,
            'DIF' : self.DIF,
            'GDD' : self.GDD,
            '온도차' : self.sub
        }
        
    def execute(self):
        data=self.data
        return_list = []
        for variable in self.var:
            try:
                temp = list(variable.keys())[0]
                standards = variable[temp]
            except:
                raise VarDataException(variable)
            for standard in standards:
                grouped_df = self.grouping_data(data, temp, standard) 
                return_list.append(grouped_df)
        return pd.concat(return_list, axis=1).reset_index()
    
    #data : 원본 데이터 , temp : 변수명, standard : 표준 [시간, 함수]
    def grouping_data(self, data, temp, standard, t_diff=2, div_DN=False, tbase=15):
        timing_key, function_key = standard
        function = self.functions_dict[function_key]
        data[temp] = DataProcess.to_numeric_or_nan(data[temp])
        target_data = data[['날짜',temp]][(data[self.timing_dict[timing_key]]==timing_key)]
        if timing_key == '전체':
            target_data = data[['날짜',temp]]
        grouped_df = target_data.groupby(pd.Grouper(key='날짜', freq=self.interval)).agg({temp: function})
        
        new_name = f'{timing_key}{function_key}{temp}'
        grouped_df.rename(columns={temp:new_name}, inplace=True)
        return grouped_df
    
    #def generating_variable(self, data, temp, standard, t_diff=2, div_DN=False, tbase=15): 
    def DIF(self, data):
        if self.is_valid(data)==False:
            return np.nan
        return max(data) - min(data)
   
    def GDD(self, data, tbase=15):
        if self.is_valid(data)==False:
            return np.nan
        temp = (max(data)+min(data))/2 - tbase
        if temp >= 0:
            return temp
        else:
            return 0
    def sub(self, data):
        if self.is_valid(data)==False:
            return np.nan
        return max(data) - min(data)
        
    def sum(self, data):
        if self.is_valid(data)==False:
            return np.nan
        return sum(data)
        
    def mean(self, data):
        if self.is_valid(data)==False:
            return np.nan
        return sum(data)/len(data)

    def min(self, data):
        if self.is_valid(data)==False:
            return np.nan
        return data.min()

    def max(self, data):
        if self.is_valid(data)==False:
            return np.nan
        return data.max()
    
    def is_valid(self, data):
        if None in data:
            return False
        elif len(data) == 0:
            return False
        else:
            return True