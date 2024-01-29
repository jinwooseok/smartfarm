import pandas as pd
import numpy as np

import json
## -------------데이터 변경 클래스-----------------
class DataProcess:

    #실수 자료를 소수점 2자리 수로 반올림
    @staticmethod
    def round_converter(data, round=2):
        #object 타입을 제외하고 소수 둘째자리로 반올림
        data[data.select_dtypes(exclude=['object']).columns] = data.select_dtypes(exclude=['object']).round(decimals = round)
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
    
    def drop_rows(data, rows):
        return data.drop(rows, axis=0)
    
    @staticmethod
    def to_numeric_or_none(series):
        numeric_series = pd.to_numeric(series, errors='coerce').astype(float)
        if numeric_series.notnull().sum() > 0:
            return numeric_series
        else:
            return None
        
    #다양한 날짜 형식 처리, 타입 처리 전엔 항상 날짜의 형태의 문자열로 처리, 날짜 열만 따로 호출함.
    def date_converter(date_series):
        date_type = date_series.dtype
        date_series = date_series.rename("날짜")
        #str, object, int, int64, datetime64의 경우 pandas to_datetime을 통해 datetime64[ns]로 변환
        try:
            if date_type == str or date_type == object:
                date_series = pd.to_datetime(date_series,format='mixed',yearfirst=True,errors='coerce')
            elif date_type in [int, np.int64]:
                date_series = pd.to_datetime(date_series.astype(str),format='mixed',yearfirst=True,errors='coerce')
            elif date_type == "datetime64[ns]" or date_type == "<M8[ns]":    
                date_series = pd.to_datetime(date_series,format='mixed',yearfirst=True,errors='coerce')
            else:
                raise ValueError
            return date_series
        except:
            raise ValueError    
        
        
    


    @staticmethod
    def dataIntegrator(data1, data2):
        data1 = data1.append(data2)
        return data1

    
    def isMinute(self):
        #분 단위인지 판별
        dateSeries = self.getDateSeries()
        if dateSeries[1] - dateSeries[0] == pd.Timedelta('0 days 00:01:00'):
            return True
        else:
            return False

    def getDateSeries(self):
        return self.data.iloc[:, self.date]
    
    
    @staticmethod
    def dataMerger(df1, df2):
        df1 = df1.append(df2)
        return df1
    
    #날짜열의 위치를 탐지. 반드시 날짜 형식이 있어야 함. 없을 시 변화없고 경고문 출력
    @staticmethod
    def dateDetecter(data):
        for i, k in enumerate(data):
            if data[k].dtype == "datetime64[ns]":
                return i
    
    @staticmethod
    def intDetecter(data):
        for i, k in enumerate(data):
            if data[k].dtype == "int64":
                return i
        return -1
    
    #컬럼명 변경
    @staticmethod
    def columnToString(df, columnIndex):
        if columnIndex != -1:
            df.iloc[:, columnIndex] = df.iloc[:, columnIndex].astype(str)
        return df
    
    #하나의 series를 받아서 결측치의 인덱스를 알려줌
    @staticmethod
    def outlier_detector(data, window_size=10, threshold=3):
        outlier_indices = []
        index_list = [i for i in range(len(data))]
        for start in range(0, len(data) - window_size):
            end = start + window_size
            if end > len(index_list):
                window_data = data.iloc[index_list[start:]]
                window_mean = window_data.mean()
                window_std = window_data.std()
                
                lower_bound = window_mean - threshold * window_std
                upper_bound = window_mean + threshold * window_std
                
                mask = (window_data < lower_bound) | (window_data > upper_bound)
                indices = np.where(mask)[0]+start
                if len(indices) == 0:
                    pass
                else:
                    for i in indices:
                        if i in index_list:
                            index_list.remove(i)
                            outlier_indices.extend(indices)
                        start -= 1
                break
            else:
                window_data = data.iloc[index_list[start:end]]    
                window_mean = window_data.mean()
                window_std = window_data.std()
                
                lower_bound = window_mean - threshold * window_std
                upper_bound = window_mean + threshold * window_std
                
                mask = (window_data < lower_bound) | (window_data > upper_bound)
                indices = [index_list[i] for i in np.where(mask)[0]+start]
                if len(indices) == 0:
                    continue
                else:
                    for i in indices:
                        if i in index_list:
                            index_list.remove(i)
                            outlier_indices.extend(indices)
                        start -= 1
        return outlier_indices
    