import numpy as np
import pandas as pd
import datetime
from .masks import *
class DailyTimeClassifier:
    def __init__(self, sun_df, date_series, t=2, noon=12):
        self.sun_df = sun_df
        self.date_series = date_series
        self.t = t
        self.noon = noon
    #일출일몰 데이터, 날짜 데이터
    def execute(self):
        sun_date = self.sun_df['날짜']
        sun_rise = self.sun_df['일출']
        sun_set = self.sun_df['일몰']
        date_series = self.date_series
        t = self.t
        
        ment = f'일출전후{t}시간'

        noon_time = datetime.datetime.strptime(f"{self.noon}:00","%H:%M").time()
        day_night_series = pd.Series(np.zeros(len(date_series)))
        srise_to_noon_series = pd.Series(np.zeros(len(date_series)))
        srise_diff_series = pd.Series(np.zeros(len(date_series)))
        
        day_night_series.name = "day_night"
        srise_to_noon_series.name = "srise_to_noon"
        srise_diff_series.name = "srise_diff"

        for i in range(len(sun_date)):
            same_month_mask = same_month_mask_generator(date_series, sun_date, i)
            #주간, 야간
            night_mask = night_mask_generator(date_series, sun_rise, sun_set, i)
            day_mask = day_mask_generator(date_series, sun_rise, sun_set, i)
            
            day_night_series[same_month_mask & night_mask] = '야간'
            day_night_series[same_month_mask & day_mask] = '주간'

            #일출부터 정오
            srise_to_noon_mask = srise_to_noon_mask_generator(date_series, sun_rise, noon_time, i)
            srise_to_noon_series[same_month_mask & srise_to_noon_mask] = '일출부터정오'

            #일출전후t시간
            tdiff_mask= tdiff_mask_generator(date_series, sun_date, sun_rise, t, i)
            srise_diff_series[same_month_mask & tdiff_mask] = ment
        
        return day_night_series, srise_to_noon_series, srise_diff_series

