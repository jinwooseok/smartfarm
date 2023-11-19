import pandas as pd
import numpy as np

import json
## -------------데이터 변경 클래스-----------------
class DataProcess:
    def __init__(self, data, date = 0, startIndex = 1):
        self.data = pd.read_json(data).iloc[int(startIndex)-1:,:].reset_index(drop=True)
        self.date = int(date)
    
    #실수 자료를 소수점 2자리 수로 반올림
    @staticmethod
    def roundConverter(data):
        #object 타입을 제외하고 소수 둘째자리로 반올림
        data[data.select_dtypes(exclude=['object']).columns] = data.select_dtypes(exclude=['object']).round(decimals = 2)
        #object와 날짜 타입은 문자로 변환
        data[data.select_dtypes(include=['object','datetime64[ns]']).columns] = data.select_dtypes(include=['object','datetime64[ns]']).astype(str)
        return data

    @staticmethod
    def dataIntegrator(data1, data2):
        data1 = data1.append(data2)
        return data1
    #데이터 변경, 결측치,이상치 처리


    #다양한 날짜 형식 처리, 타입 처리 전엔 항상 날짜의 형태의 문자열로 처리, 날짜 열만 따로 호출함.
    def dateConverter(self):
        date_type = self.getDateSeries().dtype
        self.data.rename(columns={self.data.columns[self.date]:'날짜'}, inplace=True)
        #str, object, int, int64, datetime64의 경우 pandas to_datetime을 통해 datetime64[ns]로 변환
        try:
            if date_type == str or date_type == object:
                self.data["날짜"] = pd.to_datetime(self.data["날짜"])
            elif date_type in [int, np.int64]:
                self.data["날짜"] = pd.to_datetime(self.data["날짜"].astype(str))
            elif date_type == "datetime64[ns]" or date_type == "<M8[ns]":    
                self.data["날짜"] = pd.to_datetime(self.data["날짜"])
            else:
                print("날짜 형식이 아닙니다.")
                raise ValueError
        except:
            print("날짜 형식이 아닙니다.")
            raise ValueError

    def getDateSeries(self):
        return self.data.iloc[:, self.date]
    
    def makeSummary(self):
        df = self.data.copy()
        null_count=pd.DataFrame(df.isnull().sum()).T
        null_count.index=["Null_count"]
        try:
            numeral_data = df.describe().iloc[[4,5,6,1,3,7],:]
            numeral_data.index = ["Q1","Q2","Q3","mean","min","max"]
            summary = pd.concat([null_count,numeral_data], ignore_index=False)
            summary = summary.replace({np.nan: "-"})#결측치를 처리해줌
            summary = summary.round(2)

        except IndexError:
            numeral_data = pd.DataFrame(index = ["Q1","Q2","Q3","mean","min","max"], columns = df.columns)
            summary = pd.concat([null_count,numeral_data], ignore_index=False)
            summary = summary.replace({np.nan: "-"})#결측치를 처리해줌
        summary_json = summary.to_json(orient="columns",force_ascii=False)
        #json문자열 to json 객체
        return json.loads(summary_json)
    #함수 input과 output은 데이터프레임. json변환은 따로 따로. 초기 변환은 배치처리

    def outLierDropper(self):
        data = self.data
        dropIndex = []
        for i in range(len(data.columns)):
            if data.iloc[:, i].dtype == "int64" or data.iloc[:, i].dtype == "float64":

                if len(self.outLierDetector(data.iloc[:, i])) != 0:
                    dropIndex = dropIndex+self.outLierDetector(data.iloc[:, i])
        dropIndex = list(set(dropIndex))

        self.data.drop(dropIndex, axis=0, inplace=True)
        return self.data.to_json(orient="records",force_ascii=False)
    
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
    def outLierDetector(data, window_size=10, threshold=3):
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
    