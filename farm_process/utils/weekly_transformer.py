import pandas as pd
import datetime
from farm_process.utils.masks import *
class WeeklyTransformer:
    def __init__(self, data, date_series, period):
        self.data = data
        self.date_series = date_series
        self.period = period
        
    def execute(self):
        
        first_date = self.date_series.iloc[0]
        last_date = self.date_series.iloc[-1]
        
        weeknum = int(datetime.datetime(first_date.year, first_date.month, first_date.day).strftime("%U"))
        
        standard_date = datetime.datetime.strptime(f"{first_date.year}-W{weeknum}-1", "%G-W%V-%u") #해당 주차의 마지막 날짜
        
        numeric_data = self.data.apply(pd.to_numeric, errors='coerce')
        
        temp_df = pd.DataFrame(columns=['날짜','week']+list(numeric_data.columns))
        
        i = 0
        while last_date >= standard_date:
            total_mask = daily_mask_generator(self.date_series, standard_date, self.period)
            temp = numeric_data.loc[total_mask,:].mean()
            temp['날짜'] = standard_date
            temp['week'] = weeknum
            temp_df.loc[i] = temp
            i+=1
            weeknum+=1
            if standard_date.year < (standard_date+pd.Timedelta(days=self.period)).year:
                weeknum=1

            standard_date += pd.Timedelta(days=self.period)
            
        return temp_df