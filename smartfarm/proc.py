import pandas as pd
import numpy as np
from functools import reduce
# Datetime
import datetime
from dateutil.relativedelta import relativedelta
from django.http import HttpResponse

# Crolling
import requests
import time
#etc
import warnings
warnings.filterwarnings(action='ignore')

# from geopy.geocoders import Nominatim
from .decorators import logging_time
from .utils.DataProcess import DataProcess
class ETL_system:
    def __init__(self,data,file_type,date,lat_lon,DorW,var, startRow):
        self.data = data
        self.file_type = file_type
        self.date = int(date) - 1
        self.lat, self.lon=lat_lon
        self.DorW = DorW
        self.var = var
        self.startRow = startRow

    def ETL_stream(self):
        df = DataProcess(self.data, self.date, self.startRow)
        try:
            df.dateConverter()
        except ValueError:
            raise ValueError
        if self.file_type == '환경':
            after_d=self.Envir(df)
        if self.file_type == '생육':
            after_d=self.Growth(df)
        if self.file_type == '생산량':
            after_d=self.Crop(df)
        return after_d
    
    #객체로 들어온 파일을 업데이트하여 저장    

    #환경데이터 처리함수
    def Envir(self, df):
        lon = self.lon
        lat = self.lat
    
        if self.DorW=="weeks":
        #주별데이털로 변환
            result = making_weekly2(df.data, df.date)
            result['날짜']=result['날짜'].astype('str')
        elif self.DorW == 'days':
            #시간 구별 데이터프레임 생성
            envir_date = pd.DataFrame()
            envir_date['날짜'] = df.data['날짜']
            start_month=envir_date['날짜'].astype(str)[0][0:7]
            end_month=envir_date['날짜'].astype(str)[len(envir_date)-1][0:7]
            envir_date['날짜']=pd.to_datetime(envir_date['날짜'])
            sun = get_sun(round(float(lon)),round(float(lat)),start_month,end_month)
            #낮밤구분
            nd_div=ND_div(sun, envir_date)
            #정오구분
            after_div =afternoon_div(sun, nd_div, noon=12)
            #일출일몰t시간전후
            t_diff=3
            t_div=time_div(sun,after_div, t_diff)
            #일일데이터로 변환
            generating_data=generating_dailydata(df.data, df.date, t_div,t_diff, self.var)
            result=generating_data
        else:
            result = making_weekly2(df.data, df.date, int(self.DorW))
            result['날짜']=result['날짜'].astype('str')
        result['날짜']=result['날짜'].astype('str')
        return result
    
    #생육데이터 처리함수
    def Growth(self, df):
        print("--------------생육입니다.-------------------------")
        growth_object = df.data
        date = df.date
        
        result=making_weekly2(growth_object,date)
        result['날짜']=result['날짜'].astype('str')
        return result

    #생산량데이터 처리함수
    def Crop(self, df):
        data = df.data
        date_ind=df.date
        d_ind=1
        result=y_split(data,date_ind,d_ind)
        result['날짜']=result['날짜'].astype('str')
        return result
    
    #weekly함수 실행 시에 날짜의 열이름이 '날짜'로 통일되는 점을 활용, 주별데이터, 중복없는 일일데이터 가능
    def join_data(x):
        env,prod,yld=x[0],x[1],x[2]
        env_prod=pd.merge(env,prod,left_on="날짜",right_on="날짜",how="outer")
        env_prod_yld=pd.merge(env_prod,yld,left_on="날짜",right_on="날짜",how="outer")
        return env_prod_yld


@logging_time
def get_sun(long, lati, st, ed):
    # 일출,일몰 크롤링 모듈
    #
    # long: 경도
    # lati: 위도
    # st: 시작년 시작월 "2017-10" "201710" 201710 
    # ed: 끝년 끝월 "2018-06" "201806" 201806

    # start date
    st_datetime = datetime.datetime.strptime(st, "%Y-%m")
    
    # end date
    ed_datetime = datetime.datetime.strptime(ed, "%Y-%m")
    ed_datetime = ed_datetime+relativedelta(months=1)

    # api 서비스 키
    service_key = "CHC3lP5ETp1jJorhar3RNwTH3OmFzVEWqFf2jJVkogfdbEMbXMR32QRMF1zP7EiZUsycywUpwbfp9L4nvaY8nA%3D%3D"
    

    # st~ed 까지의 일출 일몰시간 계산
    date = []; srise = []; sset = []; long_ = []; lati_ = []
    while( st_datetime != ed_datetime ):
        # api xml 추출
        URL = "http://apis.data.go.kr/B090041/openapi/service/RiseSetInfoService/getLCRiseSetInfo?serviceKey=" + \
                service_key + "&locdate=" + st_datetime.strftime("%Y%m%d") + \
                "&longitude=" + str(long) + "&latitude=" + str(lati) + "&dnYn=N"
        
        xml = requests.get(URL,verify=False).text

        # 일출 일몰 시간 추출
        sunrise = xml[xml.find('sunrise')+8:xml.find('sunrise')+12]
        sunset = xml[xml.find('sunset')+7:xml.find('sunset')+11]
        sunrise = sunrise[:2] + ":" + sunrise[2:]
        sunset = sunset[:2] + ":" + sunset[2:]
        sunrise = datetime.datetime.strptime(sunrise,"%H:%M").time()
        sunset = datetime.datetime.strptime(sunset,"%H:%M").time()

        # 각각 list에 추가
        date.append(st_datetime); srise.append(sunrise); sset.append(sunset); long_.append(long); lati_.append(lati); 
        
        # start date 증가
        st_datetime += relativedelta(months=1)


        # DataFrame 생성
        res = pd.DataFrame({
                '날짜':date,
                '일출':srise,
                '일몰':sset,
                '경도':long,
                '위도':lati
        })
    return res
@logging_time
def ND_div(sun, df):
    # 년 월 일 시간 데이터
    df2=df.copy()
    ary = np.empty(shape=(len(df['날짜']),1))
    df2['div'] = ary
    for j in range(len(sun)):
        checkDate = (sun.loc[j]['날짜'].year == df2['날짜'].dt.year) & (sun.loc[j]['날짜'].month == df2['날짜'].dt.month)
        mask_dawn = (sun.loc[j]['일출'] > df2['날짜'].dt.time) & checkDate 
        mask_afternoon = (sun.loc[j]['일출'] < df2['날짜'].dt.time) & (df2['날짜'].dt.time < sun.loc[j]['일몰']) & checkDate
        mask_night = (sun.loc[j]['일몰'] < df2['날짜'].dt.time) & checkDate
        df2.loc[mask_dawn,'div'] = '야간' 
        df2.loc[mask_afternoon,'div'] = '주간'
        df2.loc[mask_night,'div'] = '야간'
    return df2

@logging_time
def afternoon_div(sun, df, noon=12):
 # 데이터 저장
    df2=df.copy()
    ary = np.empty(shape=(len(df['날짜']),1))
    df2['day_afternoon']=ary
    noon_time = str(noon) + ":00"
    noon_time = datetime.datetime.strptime(noon_time,"%H:%M").time()
    for j in range(len(sun)):
        checkDate = (sun.loc[j]['날짜'].year == df2['날짜'].dt.year) & (sun.loc[j]['날짜'].month == df2['날짜'].dt.month)
        mask =  (sun.loc[j]['일출'] < df2['날짜'].dt.time) & (df2['날짜'].dt.time <= noon_time) & checkDate
            # sum데이터의 월과 df의 월이 같고  일출<time<noon*12 -> 일출부터 정오
        df2.loc[mask,'day_afternoon'] = '일출부터정오'
        df2=df2.replace(np.nan,'')

    return df2
#t_diff:전후시간차
@logging_time
def time_div(sun, df, t_diff):
    ment = '일출전후'+ str(t_diff)+'시간'
    df2=df.copy()
    ary = np.empty(shape=(len(df['날짜']),1))
    df2['day_thour']=ary
    
    # 일출전 t부터 일출후 t까지 시간 구분 모듈 
    for i in range(len(sun)):
        checkDate = (sun.loc[i]['날짜'].year == df2['날짜'].dt.year) & (sun.loc[i]['날짜'].month == df2['날짜'].dt.month)
        sunDate = datetime.datetime.combine(sun['날짜'][i], sun['일출'][i])
            # sum데이터의 월과 df의 월이 같고  time<일출 -> 전날 밤
        mask=((sunDate-pd.Timedelta(hours=t_diff)).time() <= df2['날짜'].dt.time) & (df2['날짜'].dt.time <= (sunDate+pd.Timedelta(hours=t_diff)).time() )&checkDate
        df2.loc[mask,'day_thour'] = ment
    df2=df2.replace(np.nan,'')
    
    return df2
#data:대상 데이터프레임
#date_ind:날짜가 포함된 열의 index
#d_ind:
#t_diff:전후시간차
@logging_time
def generating_variable(data, date_ind, d_ind, kind,t_diff , div_DN=False, tbase=15):        
    kind_div = []
    ment = '일출전후'+ str(t_diff)+'시간'

    #호출할 함수 목록
    def DIF(data):
        return max(data) - min(data)

    def GDD(data):
        temp = (max(data)+min(data))/2 - tbase
        if temp >= 0:
            return temp
        else:
            return 0

    def mean(data):
        if len(data) == 0:
            return np.nan
        return sum(data)/len(data)
    
    def min(data):
        if len(data) == 0:
            return np.nan
        return np.min(data)
    
    def max(data):
        if len(data) == 0:
            return np.nan
        return np.max(data)
    
    #입력받았을 때 호출할 함수
    functions_list = {
        '최소' : min,
        '최대' : max,
        '평균' : mean,
        '누적' : sum,
        'DIF' : DIF,
        'GDD' : GDD
    }

    for i in range(len(kind)):
        for j in range(len(functions_list)):
            if (list(functions_list.keys())[j] in kind[i]):
                kind_div.append(j)
    kind_ND = ["전체"] * len(kind)
    for i,k in enumerate(kind):
        kind_ND[i] = k[0]     
    dailyDate = data.iloc[:,date_ind].dt.date.unique()
    # 만약 div_DN이 있을 시의 코드
    # if ("야간" in kind_ND):
    #     date = date.apply(lambda x: x - dt.timedelta(days=1))

    ary = np.empty(shape=(len(dailyDate),len(kind)*len(d_ind),))
    ary[:] = np.nan

    temp_df = pd.DataFrame(ary)

    ind_name = data.columns[d_ind].tolist()

    temp_name = []
    #temp_name<-vector(length=length(kind)*length(d_ind))
    for ind in ind_name:
        for k in kind:
            if type(k) == list :
                temp_name.append(k[0]+k[1]+ind)
            else:
                temp_name.append(k + ind)
    temp_df.columns = temp_name
    #temp_df에 값 입력과정
    for i in range(len(dailyDate)):

        if ('전체' in kind_ND):
            today_ind = div_DN.index[ div_DN['날짜'].dt.date==dailyDate[i] ].tolist()
        if ('주간' in kind_ND):
            daytime_ind = div_DN.index[(div_DN['div']=='주간') & (div_DN['날짜'].dt.date==dailyDate[i])].tolist()
        if ('야간' in kind_ND):
            night_ind = div_DN.index[(div_DN['div']=='야간') & (div_DN['날짜'].dt.date==dailyDate[i])].tolist()
        if ('일출부터정오' in kind_ND):
            noon_ind = div_DN.index[(div_DN['day_afternoon']=='일출부터정오') & (div_DN['날짜'].dt.date==dailyDate[i])].tolist()
        if ('일출전후t시간' in kind_ND):
            thour_ind = div_DN.index[(div_DN['day_thour']==ment ) & (div_DN['날짜'].dt.date==dailyDate[i])].tolist()

        for j in d_ind:
            for kind_num in range(len(kind)):
                if (kind_ND[kind_num] == "주간"):
                    temp_df.iloc[i,kind_num] = functions_list[list(functions_list.keys())[kind_div[kind_num]]](data.iloc[daytime_ind,j].tolist())
                elif (kind_ND[kind_num] == "야간"):
                    temp_df.iloc[i,kind_num] = functions_list[list(functions_list.keys())[kind_div[kind_num]]](data.iloc[night_ind,j].tolist())
                elif (kind_ND[kind_num] == "전체"):
                    temp_df.iloc[i,kind_num] = functions_list[list(functions_list.keys())[kind_div[kind_num]]](data.iloc[today_ind,j].tolist())
                elif (kind_ND[kind_num] == "일출부터정오"):
                    temp_df.iloc[i,kind_num] = functions_list[list(functions_list.keys())[kind_div[kind_num]]](data.iloc[noon_ind,j].tolist())
                elif (kind_ND[kind_num] == '일출전후t시간'):
                    temp_df.iloc[i,kind_num] = functions_list[list(functions_list.keys())[kind_div[kind_num]]](data.iloc[thour_ind,j].tolist())
    temp_df = pd.concat([pd.DataFrame(dailyDate, columns=['날짜']),temp_df], axis=1)      
    return temp_df

@logging_time
def generating_dailydata(df, date_ind, t_div, t_diff, var, elsewhere=None):

    for i in range(len(var)):
        if i == 0:
            k=list(df.columns).index(list(var[i].keys())[0])
            v=list(var[i].values())[0]
            full_data = generating_variable(df, date_ind, [k], v,t_diff, t_div)
        elif i > 0:
            k=list(df.columns).index(list(var[i].keys())[0])
            v=list(var[i].values())[0]
            t = generating_variable(df, date_ind, [k], v,t_diff, t_div)
            full_data = pd.merge(full_data, t, 'right')
    
    if elsewhere is not None:
        for i in elsewhere:
            e = generating_variable(df, date_ind, [i], ["평균","최소","최대","누적","DIF","GDD"],t_diff, t_div) 
            full_data = pd.merge(full_data, e, 'right')
    return full_data


@logging_time
def making_weekly2(gdata,date_ind,interval=7):
    d = pd.DataFrame(columns=gdata.iloc[:,date_ind+1:].columns)
    day = []
    week = []
    i=0
    weeknum=0
    date=gdata["날짜"]
    lastDate=pd.to_datetime(date.iloc[-1])
    if type(date[0]) != str:
        date = date.astype('str')
    if type(date[0]) != type(pd.to_datetime(date)[0]):
        date = pd.to_datetime(date)
    if interval == 7 :
        weeknum = int(datetime.datetime(date[0].year,date[0].month,date[0].day).strftime("%U"))
        date1 = pd.to_datetime(datetime.datetime.strptime(f"{date[0].year}-W{weeknum}-1", "%G-W%V-%u")) #해당 주차의 마지막 날짜
    else:
        date1= date[0] - pd.offsets.YearBegin() # 시작 날이 포함된 년도의 1월 1일 추출 
    while True:
        mask = (pd.to_datetime(gdata.날짜) >= date1) & (pd.to_datetime(gdata.날짜) < (date1 + pd.Timedelta(days=interval)))
        g = gdata.loc[mask,:]
        if len(g) != 0:
            g = g.iloc[:,1:]
            g = g.apply('mean')
            d.loc[i]=g
            day.append(date1)
            if date1.year > (date1-pd.Timedelta(days=interval)).year:
                weeknum=0
            weeknum+=1
            week.append(weeknum)
            i+=1
        if lastDate < date1+pd.Timedelta(days=interval):
            break
        date1=date1+pd.Timedelta(days=interval)
    d.insert(0, '날짜', day)
    d.insert(1, 'week', week)
    return d

def y_split(df,date_ind,d_ind):
        if df.isnull().sum != 0:
            df.dropna()
        everyday=pd.date_range(df.iloc[0,date_ind],df.iloc[-1,date_ind])
        df2=pd.DataFrame(everyday)
        date_temp=pd.to_datetime(df.iloc[:,date_ind])#date_temp type:datetime, serialize, 2020-11-03,...
        date1=date_temp[0]#2020-11-03  #2columns dataframe
        for i in range(0,len(date_temp)-1):#serialize
            mask = (df2.iloc[:,0] > date_temp[i]) & (df2.iloc[:,0] <= date_temp[i+1])#행추출
            yield_data=df.iloc[i+1,d_ind]
            df2.loc[mask,1]=yield_data/((date_temp[i+1]-date_temp[i]).days)
        return df2