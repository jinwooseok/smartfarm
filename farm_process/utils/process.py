import pandas as pd
from weekly_transformer import WeeklyTransformer
from daily_time_classfier import DailyTimeClassifier
from get_sun_crawler import GetSunCrawler
from common.exceptions import *
from feature_generator import FeatureGenerator
from file_data.utils.process import DataProcess
#from .daily_feature_generator import DailyFeatureGenerator
class ETLProcessFactory():
    def __init__(self, data, file_type, interval, lat_lon = [38,126], var = None):
        self.data = data
        self.file_type = file_type
        self.lat, self.lon= lat_lon
        self.interval = interval
        self.var = var

    def handler(self):
        file_type = self.file_type
        interval = self.interval
        date_name = self.data.columns[0]
        self.data = self.data.dropna(subset=date_name)
        date_series = self.data.iloc[:, 0]
        self.data = DataProcess.drop_columns(self.data, [date_name])
        #날짜열은 날짜형식으로 변환 후 date_series로 관리
        date_series = DataProcess.date_converter(date_series)
        #그 후 핸들링
        if file_type=="env":
            envir_process = EnvirProcess()
            if interval=="hourly":
                return envir_process.minute_to_hour(self.data, date_series, self.lat, self.lon, self.var)
            elif interval=="daily":
                return envir_process.hour_to_daily(self.data, date_series, self.lat, self.lon, self.var)
            elif interval=="weekly":                                     
                return ETLProcessFactory.to_weekly(self.data, date_series, period=7)
        
        if file_type=="growth":
            if interval=="weekly":
                return ETLProcessFactory.to_weekly(self.data, date_series, period=7)
        
        if file_type=="output":
            output_process = OutputProcess()
            if interval=="daily":
                return output_process.y_split(self.data, date_series)
            elif interval=="weekly":                                     
                return ETLProcessFactory.to_weekly(self.data, date_series, period=7)
            return 0
        
    def to_weekly(data, date_series, period):
        result_data = WeeklyTransformer(data, date_series, period).execute()
        return result_data

class EnvirProcess:
    def minute_to_hour(self, data, date_series, lat, lon, var=None):
        concated_data = self.time_classifier(data, date_series, lat, lon)
        result_data = FeatureGenerator(concated_data, 'H', var).execute()
        return result_data
        
    def hour_to_daily(self, data, date_series, lat, lon, var = None):        
        concated_data = self.time_classifier(data, date_series, lat, lon)
        result_data = FeatureGenerator(concated_data, 'D', var).execute()
        return result_data
    
    def start_end_extractor(date_series):
        if date_series.isnull().sum() != 0:
            raise NullDateException()
        return date_series.iloc[0], date_series.iloc[-1]

    def time_classifier(self, data, date_series, lat, lon):
        start_date, end_date = EnvirProcess.start_end_extractor(date_series)
        sun_dataset = GetSunCrawler(start_date, end_date, lat, lon).execute()
        day_night_series, srise_to_noon_series, srise_diff_series = DailyTimeClassifier(sun_dataset, date_series).execute()
        
        return pd.concat([date_series, data, day_night_series, srise_to_noon_series, srise_diff_series], axis=1)
class OutputProcess:
    def y_split(self, data, date_series):
                
        everyday=pd.date_range(date_series.min(), date_series.max(), freq='D')
        return_df=pd.DataFrame({"날짜":list(everyday),"생산량":[0]*len(everyday)})
        backward_date=date_series.iloc[0]
        for idx, date in enumerate(date_series.iloc[1:]):
            mask = (return_df['날짜'] >= backward_date) & (return_df['날짜'] < date)#행추출
            return_df["생산량"][mask]=int(data.iloc[idx])/(date-backward_date).days
            backward_date=date

        return return_df

    
