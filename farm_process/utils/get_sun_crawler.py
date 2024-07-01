"""
일출, 일몰 크롤링 모듈
"""
import datetime
import pandas as pd
import requests
from dateutil.relativedelta import relativedelta
from common.exceptions import *
from common.decorators import logging_time
class GetSunCrawler():
    """
    일출, 일몰 데이터를 크롤링하는 클래스
    
    메서드
    - __init__(self, start_date, end_date, lati=38, long=126) : 초기화 메서드
    - execute(self) : 실행 메서드
    - get_sun_from_response(response) : 응답에서 일출, 일몰 데이터 추출 메서드
    """
    def __init__(self, start_date, end_date, lati=38, long=126):
        """
        초기화 메서드
        
        매개변수
        - start_date : 시작 날짜
        - end_date : 종료 날짜
        - lati : 위도
        - long : 경도
        """
        self.long = long
        self.lati = lati
        self.start_date = start_date
        self.end_date = end_date
        # 공공데이터포털 서비스키 - 현재 유효하지 않음
        self.service_key = "KrL1x60Wlerl6EMB6sls2UUFYHp5PDj0jaRyBUDt%2Fh3ginr04Btpg%2BF8hCjIsE%2FyXHan%2BC7J3IkPLCekCdHT6A%3D%3D"

    @logging_time
    def execute(self):
        """
        실행 메서드
        
        로직 
        1. 시작, 종료 날짜를 가져온다.
        2. 시작, 종료 월을 가져온다.
        3. API 요청을 통해 일출, 일몰 데이터를 가져온다.
        4. response 데이터의 형태를 변환한다.
        4. 데이터를 반환한다.
        """
        start_date = self.start_date        
        end_date = self.end_date
        start_month, end_month = self.get_start_end_month(start_date, end_date)
        data_list = []
        # 시작 월부터 종료 월까지 반복
        while(start_month != end_month):
            # API 요청 폼 생성
            URL = self.api_form(self.service_key, start_month, self.long, self.lati)
            # API 요청
            response = requests.get(URL, verify=False).text
            # 응답에서 일출, 일몰 데이터 추출
            srise, sset = self.get_sun_from_response(response)
            data_list.append([start_month, srise, sset])
            # start date 증가
            start_month += relativedelta(months=1)
        return pd.DataFrame(data_list, columns=['날짜', '일출', '일몰'])

    @staticmethod
    def get_sun_from_response(response):
        """
        응답에서 일출, 일몰 데이터 추출 메서드
        
        매개변수
        - response : 응답 데이터
        """
        sunrise = response[response.find('sunrise')+8:response.find('sunrise')+12]
        sunset = response[response.find('sunset')+7:response.find('sunset')+11]
          
        sunrise = sunrise[:2] + ":" + sunrise[2:]
        sunset = sunset[:2] + ":" + sunset[2:]
        # try : 일출, 일몰 데이터 변환 except : api 관련 예외
        try:
            sunrise = datetime.datetime.strptime(sunrise,"%H:%M").time()
            sunset = datetime.datetime.strptime(sunset,"%H:%M").time()
        except:
            raise GetSunApiException()
        return sunrise, sunset

    @staticmethod
    def api_form(service_key, date, long, lati):
        """
        API 요청 폼 생성 메서드
        """
        URL = "http://apis.data.go.kr/B090041/openapi/service/RiseSetInfoService/getLCRiseSetInfo?serviceKey=" + \
                        service_key + "&locdate=" + date.strftime("%Y%m%d") + \
                        "&longitude=" + str(long) + "&latitude=" + str(lati) + "&dnYn=N"
        return URL

    @staticmethod
    def get_start_end_month(start_date, end_date):
        """
        시작, 종료 월을 가져오는 메서드
        """
        start_month = GetSunCrawler.get_first_of_month(start_date)
        end_month =  GetSunCrawler.get_first_of_month(end_date+relativedelta(months=1))

        return start_month, end_month
    
    @staticmethod
    def get_first_of_month(input_date):
        """
        월의 첫 날을 가져오는 메서드
        """
        return datetime.datetime(input_date.year, input_date.month, 1)