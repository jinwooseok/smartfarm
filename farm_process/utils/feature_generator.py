"""
변수 생성기
- 변수 생성에 필요한 데이터를 조합해 새로운 변수 생성을 수행함
"""
import pandas as pd
import numpy as np
from farm_process.utils.masks import *
from common.exceptions import *
from common.decorators import logging_time
from file_data.utils.process import DataProcess
class FeatureGenerator:
    """
    변수 생성기 클래스
    
    메서드
    - __init__(self, data, interval, var=None) : 초기화 메서드
    - execute(self) : 실행 메서드
    """
    def __init__(self, data, interval, var=None):
        """
        초기화 메서드
        
        매개변수
        - data : 데이터
        - interval : 시간 간격
        - var : 변수 리스트
        """
        self.data = data
        self.date_series = data['날짜']
        self.var = var
        self.interval= interval
        # tbase : 기준 온도
        self.tbase = 15
        # timing_dict : 시간대 딕셔너리
        self.timing_dict = {
            '전체' : 'day_night',
            '주간' : 'day_night',
            '야간' : 'day_night',
            '일출부터정오' : 'srise_to_noon',
            '일출전후2시간' : 'srise_diff'
        }
        # 함수 딕셔너리
        self.functions_dict = {
            '최소' : self.min,
            '최대' : self.max,
            '평균' : self.mean,
            '누적' : self.sum,
            'DIF' : self.DIF,
            'GDD' : self.GDD,
            '온도차' : self.sub
        }
    @logging_time
    def execute(self):
        """
        실행 메서드 - 기본 변수들에서 파생 변수 생성
        
        실행 로직
        1. 변수 리스트에서 변수를 가져온다.
        2. 변수를 생성한다.
        3. 생성된 변수를 반환한다.
        """
        data=self.data
        return_list = []
        for variable in self.var: # 변수 리스트에서 변수를 가져온다. except -> 변수 데이터와 관련된 모든 예외
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
    def grouping_data(self, data, temp, standard):
        """
        데이터 그룹화 메서드
        
        매개변수
        - data : 데이터
        - temp : 변수명
        - standard : 표준 [시간, 함수]
        """
        timing_key, function_key = standard
        function = self.functions_dict[function_key]
        data[temp] = DataProcess.to_numeric_or_nan(data[temp])
        if timing_key == '전체':
            target_data = data[['날짜',temp]]
        else:
            target_data = data[['날짜',temp]][(data[self.timing_dict[timing_key]]==timing_key)]
        # 그룹화된 데이터 생성
        grouped_df = target_data.groupby(pd.Grouper(key='날짜', freq=self.interval)).agg({temp : function})
        # 새로운 변수명 생성
        new_name = f'{timing_key}{function_key}{temp}'
        grouped_df.rename(columns={temp:new_name}, inplace=True)
        return grouped_df
    def DIF(self, temp):
        """
        온도차 계산 메서드
        """
        if self.is_valid(temp) is False:
            return np.nan
        # 주간 평균과 야간 평균 계산. except -> temp데이터가 없는 경우 nan 반환
        try:
            day_mean = temp[self.data['day_night'] == "주간"].mean()
            night_mean = temp[self.data['day_night'] == "야간"].mean()
        except:
            return np.nan
        # 주간 평균 - 야간 평균 계산
        return day_mean - night_mean

    def GDD(self, data):
        """
        GDD 계산 메서드 -> (최대 온도 + 최소 온도) / 2 - 기준 온도
        """
        if self.is_valid(data) is False:
            return np.nan
        temp = (max(data)+min(data))/2 - self.tbase
        if temp >= 0:
            return temp
        else:
            return 0
    def sub(self, data):
        """
        온도차 계산 메서드
        """
        if self.is_valid(data) is False:
            return np.nan
        return max(data) - min(data)

    def sum(self, data):
        if self.is_valid(data) is False:
            return np.nan
        return sum(data)

    def mean(self, data):
        if self.is_valid(data) is False:
            return np.nan
        return sum(data)/len(data)

    def min(self, data):
        if self.is_valid(data) is False:
            return np.nan
        return data.min()

    def max(self, data):
        if self.is_valid(data) is False:
            return np.nan
        return data.max()

    def is_valid(self, data):
        """
        데이터 유효성 검사 메서드
        if 데이터에 None이 포함되어 있다 : False
        elif 데이터의 개수가 0이다 : False
        else : True
        """
        if None in data:
            return False
        elif len(data) == 0:
            return False
        else:
            return True