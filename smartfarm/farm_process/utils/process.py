import pandas as pd
from .weekly_transformer import WeeklyTransformer
from .daily_time_classfier import DailyTimeClassifier
from .get_sun_crawler import GetSunCrawler
from ..exceptions.exceptions import *
from .daily_feature_generator import DailyFeatureGenerator
from .hour_feature_generator import HourFeatureGenerator
from ...file_data.utils.process import DataProcess
#from .daily_feature_generator import DailyFeatureGenerator
class ETLProcessFactory():
    def __init__(self, data, file_type, date_column, interval, lat_lon = [38,126], var = None):
        self.data = data
        self.file_type = file_type
        self.date_column = date_column - 1
        self.lat, self.lon= lat_lon
        self.interval = interval
        self.var = var

    def handler(self):
        file_type = self.file_type
        interval = self.interval

        self.data = self.data.dropna(subset=[self.data.columns[self.date_column]])
        
        #날짜열 추출
        if self.date_column < 0 or self.date_column >= len(self.data.columns):
            raise DateColumnException()
        date_series = self.data.iloc[:,self.date_column]
        
        #날짜열 드롭. 방해됨
        date_column_index = self.date_column
        self.data = DataProcess.drop_columns(self.data, [self.data.columns[date_column_index]])
        #날짜열은 날짜형식으로 변환 후 date_series로 관리
        date_series = DataProcess.date_converter(date_series)
        #그 후 핸들링
        if file_type=="env":
            if interval=="hourly":
                return EnvirProcess.minute_to_hour(self.data, date_series
                                                  , self.lat, self.lon, self.var)
            elif interval=="daily":
                return EnvirProcess.hour_to_daily(self.data, date_series
                                                  , self.lat, self.lon, self.var)
            elif interval=="weekly":                                     
                period = 7
                return ETLProcessFactory.to_weekly(self.data, date_series, period)
        if file_type=="growth":
            if interval=="weekly":
                period = 7
                return ETLProcessFactory.to_weekly(self.data, date_series, period)
        if file_type=="output":
            return 0
        
    def to_weekly(data, date_series, period):
        result_data = WeeklyTransformer(data, date_series, period).execute()
        return result_data

class EnvirProcess:
    @staticmethod
    def minute_to_hour(data, date_series, lat, lon, var=None):
        start_date, end_date = EnvirProcess.start_end_extractor(date_series)
        sun_dataset = GetSunCrawler(start_date, end_date, lat, lon).execute()
        day_night_series, srise_to_noon_series, srise_diff_series = DailyTimeClassifier(sun_dataset, date_series).execute()
        
        concated_data = pd.concat([date_series, data, day_night_series, srise_to_noon_series, srise_diff_series], axis=1)
        result_data = HourFeatureGenerator(concated_data, var).execute()
        
        return result_data
        
    @staticmethod
    def hour_to_daily(data, date_series, lat, lon, var = None):        
        start_date, end_date = EnvirProcess.start_end_extractor(date_series)
        sun_dataset = GetSunCrawler(start_date, end_date, lat, lon).execute()
        day_night_series, srise_to_noon_series, srise_diff_series = DailyTimeClassifier(sun_dataset, date_series).execute()
        
        concated_data = pd.concat([date_series, data, day_night_series, srise_to_noon_series, srise_diff_series], axis=1)
        result_data = DailyFeatureGenerator(concated_data, var).execute()
        
        return result_data
    
    @staticmethod
    def start_end_extractor(date_series):
        if date_series.isnull().sum() != 0:
            raise NullDateException()
        return date_series.iloc[0], date_series.iloc[-1]


# class OutputProcess(ETLProcess):
#     def execute():
#         data = df.data
#         date=df.date
#         d_ind=1
#         if self.DorW=="days":
#             result=y_split(data,date,d_ind)
#             result['날짜']=result['날짜'].astype('str')
#         if self.DorW=="weeks":
#             result=y_split(data,date,d_ind)
#             result = making_weekly2(data, date)
#             result['날짜']=result['날짜'].astype('str')
#         return result
#         pass 
    
#     @staticmethod
#     def y_split(df,date_ind,d_ind):
#         if df.isnull().sum != 0:
#                 df.dropna()
#         everyday=pd.date_range(df.iloc[0,date_ind],df.iloc[-1,date_ind])
#         df2=pd.DataFrame({"날짜":everyday})
#         date_temp=pd.to_datetime(df.iloc[:,date_ind])#date_temp type:datetime, serialize, 2020-11-03,...
#         for i in range(0,len(date_temp)-1):#serialize
#                 mask = (df2.iloc[:,0] > date_temp[i]) & (df2.iloc[:,0] <= date_temp[i+1])#행추출
#                 yield_data=df.iloc[i+1,d_ind]
#                 print(yield_data)
#                 df2.loc[mask,"생산량"]=int(yield_data)/((date_temp[i+1]-date_temp[i]).days)

#         return df2

    
