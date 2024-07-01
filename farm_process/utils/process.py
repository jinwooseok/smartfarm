"""
데이터 전처리 파이프라인을 생성하는 클래스
"""
import pandas as pd
from farm_process.utils.weekly_transformer import WeeklyTransformer
from farm_process.utils.daily_time_classfier import DailyTimeClassifier
from farm_process.utils.get_sun_crawler import GetSunCrawler
from farm_process.utils.feature_generator import FeatureGenerator
from common.exceptions import *
from file_data.utils.process import DataProcess
class ETLProcessFactory():
    """
    ETL 프로세스를 생성하는 클래스
    
    메서드
    - __init__(self, data, file_type, interval, lat_lon = [38,126], var = None) : 초기화 메서드
    - handler(self) : 핸들러 메서드
    - to_weekly(data, date_series, period) : 주간 데이터로 변환하는 메서드
    """
    def __init__(self, data, file_type, interval, lat_lon = [38,126], var = None):
        """
        초기화 메서드
        
        매개변수
        - data : 데이터
        - file_type : 파일 타입
        - lat_lon : 위도, 경도
        - interval : 시간 간격
        - var : 변수 리스트
        """
        self.data = data
        self.file_type = file_type
        self.lat, self.lon= lat_lon
        self.interval = interval
        self.var = var

    def handler(self):
        """
        핸들러 메서드
        
        로직
        1. 파일 타입에 따라 분기(환경, 생육, 생산)
        2. 시간 간격에 따라 분기(시간별, 일별, 주간)
        3. 각각의 프로세스를 실행
        4. 결과 반환
        """
        file_type = self.file_type
        interval = self.interval
        date_name = self.data.columns[0]
        self.data = self.data.dropna(subset=date_name)
        date_series = self.data.iloc[:, 0]
        #날짜열 제거
        self.data = DataProcess.drop_columns(self.data, [date_name])
        #날짜열은 날짜형식으로 변환 후 date_series로 관리
        date_series = DataProcess.date_converter(date_series)
        #환경 타입 파일일 경우
        if file_type=="env":
            envir_process = EnvirProcess()
            if interval=="hourly":
                return envir_process.minute_to_hour(self.data, date_series,
                                                    self.lat, self.lon, self.var)
            elif interval=="daily":
                return envir_process.hour_to_daily(self.data, date_series,
                                                   self.lat, self.lon, self.var)
            elif interval=="weekly":
                return ETLProcessFactory.to_weekly(self.data, date_series, period=7)
        #생육 타입 파일일 경우
        if file_type=="growth":
            if interval=="weekly":
                return ETLProcessFactory.to_weekly(self.data, date_series, period=7)
        #생산 타입 파일일 경우
        if file_type=="output":
            output_process = OutputProcess()
            if interval=="daily":
                return output_process.y_split(self.data, date_series)
            elif interval=="weekly":
                return ETLProcessFactory.to_weekly(self.data, date_series, period=7)

    def to_weekly(data, date_series, period):
        """
        모든 타입의 데이터를 주간 데이터로 변환하는 메서드 (WeeklyTransformer 호출)
        """
        result_data = WeeklyTransformer(data, date_series,
                                        period).execute()
        return result_data

class EnvirProcess:
    """
    환경 데이터 전처리 클래스
    
    메서드
    - minute_to_hour(self, data, date_series, lat, lon, var=None) : 분 단위 데이터를 시간 단위 데이터로 변환
    - hour_to_daily(self, data, date_series, lat, lon, var = None) : 시간 단위 데이터를 일 단위 데이터로 변환
    - start_end_extractor(date_series) : 시작, 끝 날짜 추출
    - time_classifier(self, data, date_series, lat, lon) : 데이터에 시간대 분류
    """
    def minute_to_hour(self, data, date_series, lat, lon, var=None):
        """
        분 단위 데이터를 시간 단위 데이터로 변환하는 메서드

        매개변수
        - data : 데이터
        - date_series : 날짜 데이터
        - lat : 위도
        - lon : 경도
        - var : 변수 리스트
        """
        concated_data = self.time_classifier(data, date_series, lat, lon)
        result_data = FeatureGenerator(concated_data, 'H', var).execute()
        return result_data
        
    def hour_to_daily(self, data, date_series, lat, lon, var = None):   
        """
        시간 단위 데이터를 일 단위 데이터로 변환하는 메서드
        
        매개변수
        - data : 데이터
        - date_series : 날짜 데이터
        - lat : 위도
        - lon : 경도
        - var : 변수 리스트
        """     
        concated_data = self.time_classifier(data, date_series, lat, lon)
        result_data = FeatureGenerator(concated_data, 'D', var).execute()
        return result_data
    
    def start_end_extractor(date_series):
        """
        시작, 끝 날짜 추출 메서드
        """
        if date_series.isnull().sum() != 0:
            raise NullDateException()
        return date_series.iloc[0], date_series.iloc[-1]

    def time_classifier(self, data, date_series, lat, lon):
        """
        데이터에 시간대 분류하는 메서드
        """
        start_date, end_date = EnvirProcess.start_end_extractor(date_series)
        sun_dataset = GetSunCrawler(start_date, end_date, lat, lon).execute()
        day_night_series, srise_to_noon_series, srise_diff_series = DailyTimeClassifier(sun_dataset, date_series).execute()
        
        return pd.concat([date_series, data, day_night_series, srise_to_noon_series, srise_diff_series], axis=1)
class OutputProcess:
    """
    생산 데이터 전처리 클래스
    """
    def y_split(self, data, date_series):
        """
        데이터를 일별로 분할하는 메서드
        """
        everyday=pd.date_range(date_series.min(), date_series.max(), freq='D')
        return_df=pd.DataFrame({"날짜":list(everyday),"생산량":[0]*len(everyday)})
        backward_date=date_series.iloc[0]
        for idx, date in enumerate(date_series.iloc[1:]):
            mask = (return_df['날짜'] >= backward_date) & (return_df['날짜'] < date)#행추출
            return_df["생산량"][mask]=int(data.iloc[idx])/(date-backward_date).days
            backward_date=date
        return return_df
