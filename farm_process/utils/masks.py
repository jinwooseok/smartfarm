"""
날짜와 관련된 필터 마스크들을 모아놓은 폴더
"""
import pandas as pd
import datetime
def timing_mask_generator(timing_df, timing):
    """
    시간 데이터를 비교하여 마스크를 생성하는 함수
    """
    return timing_df == timing

def daily_mask_generator(date_series, standard_date, interval):
    """
    일별 마스크 생성 함수 -> 날짜가 standard_date 이상 interval 미만인 데이터를 필터링
    """
    return (date_series.dt.date >= standard_date.date()) & (date_series.dt.date < (standard_date + pd.Timedelta(days=interval)).date())

def hour_mask_generator(date_series, standard_date, interval):
    """
    시간별 마스크 생성 함수 -> 시간이 standard_date 이상 interval 미만인 데이터를 필터링
    """
    return (date_series.dt.hour >= standard_date.hour) & (date_series.dt.hour < (standard_date + pd.Timedelta(hours=interval)).hour)

def same_month_mask_generator(date_series, sun_date, i):
    """
    같은 달 마스크 생성 함수 -> sun_date의 i번째 데이터와 date_series의 달이 같은 데이터를 필터링
    """
    return (sun_date.iloc[i].year == date_series.dt.year) & (sun_date.iloc[i].month == date_series.dt.month)

def night_mask_generator(date_series, sun_rise, sun_set, i):
    """
    야간 마스크 생성 함수 -> 일출보다 이르거나 일몰보다 늦은 데이터를 필터링
    """
    return (sun_rise.iloc[i] > date_series.dt.time) | (sun_set.iloc[i] < date_series.dt.time)

def day_mask_generator(date_series, sun_rise, sun_set, i):
    """
    주간 마스크 생성 함수 -> 일출보다 늦고 일몰보다 이른 데이터를 필터링
    """
    return (sun_rise.iloc[i] < date_series.dt.time) & (date_series.dt.time < sun_set.iloc[i])

def srise_to_noon_mask_generator(date_series, sun_rise, noon_time, i):
    """
    일출부터 정오 마스크 생성 함수 -> 일출부터 정오까지의 데이터를 필터링
    """
    return (sun_rise.iloc[i] < date_series.dt.time) & (date_series.dt.time <= noon_time)

def tdiff_mask_generator(date_series, sun_date, sun_rise, t, i):
    """
    일출전후t시간 마스크 생성 함수 -> 일출 전후 t시간의 데이터를 필터링
    """
    combined_sunrise = datetime.datetime.combine(sun_date.iloc[i], sun_rise.iloc[i])
    return ((combined_sunrise-pd.Timedelta(hours=t)).time() <= date_series.dt.time) & (date_series.dt.time <= (combined_sunrise+pd.Timedelta(hours=t)).time())

def total_mask_generator(mask_list):
        """
        여러 마스크를 조합하는 함수
        """
        total_mask = mask_list[0]
        for mask in mask_list[1:]:
            total_mask = total_mask & mask
        return total_mask