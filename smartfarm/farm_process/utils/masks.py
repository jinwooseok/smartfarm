import pandas as pd
import datetime
def timing_mask_generator(timing_df, timing):
    return timing_df == timing

def daily_mask_generator(date_series, standard_date, interval):
    return (date_series.dt.date >= standard_date.date()) & (date_series.dt.date < (standard_date + pd.Timedelta(days=interval)).date())

def hour_mask_generator(date_series, standard_date, interval):
    return (date_series.dt.hour >= standard_date.hour) & (date_series.dt.hour < (standard_date + pd.Timedelta(hours=interval)).hour)

def same_month_mask_generator(date_series, sun_date, i):
    return (sun_date.iloc[i].year == date_series.dt.year) & (sun_date.iloc[i].month == date_series.dt.month)

def night_mask_generator(date_series, sun_rise, sun_set, i):
    return (sun_rise.iloc[i] > date_series.dt.time) | (sun_set.iloc[i] < date_series.dt.time)

def day_mask_generator(date_series, sun_rise, sun_set, i):
    return (sun_rise.iloc[i] < date_series.dt.time) & (date_series.dt.time < sun_set.iloc[i])

def srise_to_noon_mask_generator(date_series, sun_rise, noon_time, i):
    return (sun_rise.iloc[i] < date_series.dt.time) & (date_series.dt.time <= noon_time)

def tdiff_mask_generator(date_series, sun_date, sun_rise, t, i):
    combined_sunrise = datetime.datetime.combine(sun_date.iloc[i], sun_rise.iloc[i])
    return ((combined_sunrise-pd.Timedelta(hours=t)).time() <= date_series.dt.time) & (date_series.dt.time <= (combined_sunrise+pd.Timedelta(hours=t)).time())

def total_mask_generator(mask_list):
        total_mask = mask_list[0]
        for mask in mask_list[1:]:
            total_mask = total_mask & mask
        return total_mask