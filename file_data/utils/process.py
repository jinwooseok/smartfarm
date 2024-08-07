import pandas as pd
import numpy as np
import json
from common.exceptions import *
from common.decorators import logging_time
## -------------데이터 변경 클래스-----------------
class DataProcess:

    #실수 자료를 소수점 2자리 수로 반올림
    @staticmethod
    def round_converter(data, round=2):
        #object 타입을 제외하고 소수 둘째자리로 반올림
        data[data.select_dtypes(exclude=['object']).columns] = data.select_dtypes(exclude=['object']).round(round)
        #object와 날짜 타입은 문자로 변환
        data[data.select_dtypes(include=['object','datetime64[ns]']).columns] = data.select_dtypes(include=['object','datetime64[ns]']).astype(str)
        return data
    
    @staticmethod
    def nan_to_string(data, string=""):
        return data.replace({np.nan: string})
    
    @staticmethod
    def df_to_json_string(data, orient="records"):
        return data.to_json(orient=orient,force_ascii=False)

    @staticmethod
    def df_to_json_object(data, orient="records"):
        return json.loads(data.to_json(orient=orient,force_ascii=False))
    #데이터 변경, 결측치,이상치 처리
    
    @staticmethod
    def drop_columns(data, columns):
        return data.drop(columns, axis=1)
    @staticmethod
    def drop_rows(data, rows):
        return data.drop(rows, axis=0)
    
    @staticmethod
    def to_numeric_or_none(series):
        numeric_series = pd.to_numeric(series, errors='coerce').astype(float)
        if numeric_series.notnull().sum() > 0:
            return numeric_series
        else:
            return None
        
    @staticmethod
    def to_numeric_or_nan(series):
        numeric_series = pd.to_numeric(series, errors='coerce').astype(float)
        if numeric_series.notnull().sum() > 0:
            return numeric_series
        else:
            return np.nan
        
    #다양한 날짜 형식 처리, 타입 처리 전엔 항상 날짜의 형태의 문자열로 처리, 날짜 열만 따로 호출함.
    @staticmethod
    def date_converter(date_series):
        date_type = date_series.dtype
        date_series = date_series.rename("날짜")
        #str, object, int, int64, datetime64의 경우 pandas to_datetime을 통해 datetime64[ns]로 변환
        try:
            if date_type == str or date_type == object:
                date_series = pd.to_datetime(date_series,format='mixed',yearfirst=True,errors='coerce')
            elif date_type in [int, np.int64]:
                date_series = pd.to_datetime(date_series.astype(str),format='mixed',yearfirst=True,errors='coerce')
            # elif date_type in [float, np.float64]:
            #     excel_base_date = datetime(1899, 12, 30)
            #     excel_base_date + timedelta(days=excel_date)
            #     df['날짜열'] = df['날짜열'].apply(convert_excel_date)
            elif date_type == "datetime64[ns]" or date_type == "<M8[ns]":    
                date_series = pd.to_datetime(date_series,format='mixed',yearfirst=True,errors='coerce')
            else:
                raise DateConverterException()
            return date_series
        except:
            raise DateConverterException() 
        
    #결측치 처리
    @staticmethod
    def nan_handler(data, method="drop"):
        if method == "drop":
            return data.dropna()
        elif method == "fill":
            return data.fillna(0)
        else:
            return data.fillna(method)
    

    #하나의 series를 받아서 결측치의 인덱스를 알려줌
    @logging_time
    @staticmethod
    def outlier_detector(data, window_size=10, threshold=3):
        rolling_mean = data.rolling(window=window_size, min_periods=1).mean()
        rolling_std = data.rolling(window=window_size, min_periods=1).std()
        lower_bound = rolling_mean - threshold * rolling_std
        upper_bound = rolling_mean + threshold * rolling_std

        outlier_mask = (data < lower_bound) | (data > upper_bound)

        outlier_indices = np.where(outlier_mask)[0]
        return outlier_indices
        