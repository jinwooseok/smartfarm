import datetime
import pandas as pd
import requests
from dateutil.relativedelta import relativedelta
from ..exceptions.date_exceptions import *
# 일출,일몰 크롤링 모듈
        #
        # long: 경도
        # lati: 위도
        # st: 시작년 시작월 "2017-10" "201710" 201710 
        # ed: 끝년 끝월 "2018-06" "201806" 201806
class GetSunCrawler():
    def __init__(self, start_date, end_date, lati=38, long=126):
        self.long = long
        self.lati = lati
        self.start_date = start_date
        self.end_date = end_date
        self.service_key = "KrL1x60Wlerl6EMB6sls2UUFYHp5PDj0jaRyBUDt%2Fh3ginr04Btpg%2BF8hCjIsE%2FyXHan%2BC7J3IkPLCekCdHT6A%3D%3D"
        
    def execute(self):
        start_date = self.start_date        
        end_date = self.end_date

        start_month, end_month = self.get_start_end_month(start_date, end_date)

        data_list = []

        while(start_month != end_month):
            URL = self.api_form(self.service_key, start_month, self.long, self.lati)
            response = requests.get(URL, verify=False).text
            srise, sset = self.get_sun_from_response(response)
            data_list.append([start_month, srise, sset])
            # start date 증가
            start_month += relativedelta(months=1)

        return pd.DataFrame(data_list, columns=['날짜', '일출', '일몰'])

    @staticmethod
    def get_sun_from_response(response):
        # 일출 일몰 시간 추출
        sunrise = response[response.find('sunrise')+8:response.find('sunrise')+12]
        sunset = response[response.find('sunset')+7:response.find('sunset')+11]
          
        sunrise = sunrise[:2] + ":" + sunrise[2:]
        sunset = sunset[:2] + ":" + sunset[2:]
        try:
            sunrise = datetime.datetime.strptime(sunrise,"%H:%M").time()
            sunset = datetime.datetime.strptime(sunset,"%H:%M").time()
        except:
            raise GetSunApiException()
        return sunrise, sunset

    @staticmethod
    def api_form(service_key, date, long, lati):
        URL = "http://apis.data.go.kr/B090041/openapi/service/RiseSetInfoService/getLCRiseSetInfo?serviceKey=" + \
                        service_key + "&locdate=" + date.strftime("%Y%m%d") + \
                        "&longitude=" + str(long) + "&latitude=" + str(lati) + "&dnYn=N"
        return URL
    
    @staticmethod
    def get_start_end_month(start_date, end_date):
        # start date
        start_month = GetSunCrawler.get_first_of_month(start_date)
        end_month =  GetSunCrawler.get_first_of_month(end_date+relativedelta(months=1))

        return start_month, end_month
    
    @staticmethod
    def get_first_of_month(input_date):
        return datetime.datetime(input_date.year, input_date.month, 1)