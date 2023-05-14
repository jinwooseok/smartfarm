import pandas as pd
import numpy as np
from functools import reduce
# Datetime
import datetime
from dateutil.relativedelta import relativedelta

# Crolling
import requests
#etc
import warnings
warnings.filterwarnings(action='ignore')

#day to week
from urllib.parse import urlencode, quote_plus, unquote
# from geopy.geocoders import Nominatim
from .decorators import logging_time

from  .utils import DataProcess
# def geocoding(address):
#     geo_local = Nominatim(user_agent='South Korea')
#     try:
#         geo = geo_local.geocode(address)
#         x_y = [geo.latitude, geo.longitude]
#         return x_y

#     except:
#         return [0,0]
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
    service_key = "3zMUzXFBb6NM1NuuJ7gtxWOoq5%2FctdtXx8HyBMzAPcE65bev5C6qy9E2e5CJphMtY%2FumqtkPg%2FEmj3OmbJFrdw%3D%3D"
    

    # st~ed 까지의 일출 일몰시간 계산
    date = []; srise = []; sset = []; long_ = []; lati_ = []
    while( st_datetime != ed_datetime ):
        
        # api xml 추출
        URL = "https://apis.data.go.kr/B090041/openapi/service/RiseSetInfoService/getLCRiseSetInfo?serviceKey=" + \
                service_key + "&locdate=" + st_datetime.strftime("%Y%m%d") + \
                "&longitude=" + str(long) + "&latitude=" + str(lati) + "&dnYn=N"
        xml = requests.get(URL,verify=False).text
        
        # 일출 일몰 시간 추출
        sunrise = xml[xml.find('sunrise')+8:xml.find('sunrise')+12]
        sunset = xml[xml.find('sunset')+7:xml.find('sunset')+11]
        
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
    sun2=sun.copy()
    df_split=df['날짜'].str.split(" ", expand=True) # 데이터를 연도와 시간으로 분리
    df2['날짜']=df_split[0].replace('-','',regex=True) # '-' 제거 
    df2['time']=pd.to_numeric(df_split[1].replace(':','',regex=True)) # ':' 제거 후 int로 타입변환
    
    # 크롤링 데이터
    sun2.dtypes
    sun2[['일출','일몰']]=sun2[['일출','일몰']].astype(int) # int로 타입변환
    sun2['날짜']=sun2['날짜'].astype(str) # str로 타입변환
    sun2['날짜']=sun2['날짜'].replace('-','',regex=True).str[0:6]
    # 전날 밤, 주간, 야간 구분
    ary = np.empty(shape=(len(df['날짜']),3))

    df_return = pd.DataFrame(ary)
    df_return.columns = ['날짜','time','div']
    df_return.iloc[:,0]=df2['날짜']
    df_return.iloc[:,1]=df2['time']
    df2['날짜']=df2['날짜'].str[0:6]

    for j in range(len(sun)):
        mask_dawn = (sun2.loc[j]['일출'] > df2['time']) & (sun2.loc[j]['날짜'] == df2['날짜'])
        mask_afternoon = (sun2.loc[j]['일출'] < df2['time']) & (df2['time'] < sun2.loc[j]['일몰']) & (sun2.loc[j]['날짜'] == df2['날짜'])
        mask_night = (sun2.loc[j]['일몰'] < df2['time']) & (sun2.loc[j]['날짜'] == df2['날짜'])
        df_return.loc[mask_dawn,'div'] = '야간' 
        df_return.loc[mask_afternoon,'div'] = '주간'
        df_return.loc[mask_night,'div'] = '야간'

    
    return df_return
@logging_time
def afternoon_div(sun, df, noon=12):
 # 데이터 저장
    df2=df.copy()
    sun2=sun.copy()
    ary = np.empty(shape=(len(df['날짜']),1))
    df2['day_afternoon']=ary
    df_return = df2.copy()
    sun2['날짜'] = sun2['날짜'].astype(str) # str로 타입변환
    sun2['날짜'] = sun2['날짜'].replace('-','',regex=True).str[0:6]
    df2['날짜'] = df2['날짜'].str[0:6]
    df2['time'] = df2['time'].astype(int)
    sun2['일출'] = sun2['일출'].astype(int)
    sun2['날짜'] = sun2['날짜'].astype(int)
    df2['날짜']=df2['날짜'].astype(int)
    for j in range(len(sun2)):
        mask =  (sun2.loc[j]['일출'] < df2['time']) & (df2['time'] <= noon*100) & ( sun2.loc[j]['날짜'] == df2['날짜'])
            # sum데이터의 월과 df의 월이 같고  일출<time<noon*12 -> 일출부터 정오
        df_return.loc[mask,'day_afternoon'] = '일출부터정오'
    
        df_return=df_return.replace(np.nan,'')
            # 나머지
    
    return df_return
#t_diff:전후시간차
@logging_time
def time_div(sun, df, t_diff):
    ment = '일출전후'+ str(t_diff)+'시간'
    df2=df.copy()
    sun2=sun.copy()
    ary = np.empty(shape=(len(df['날짜']),1))
    ary[:] = np.nan
    df2['day_thour']=ary
    df_return = df2.copy()
    sun2['날짜']=sun2['날짜'].astype(str) # str로 타입변환
    sun2['날짜']=sun2['날짜'].replace('-','',regex=True).str[0:6]
    df2['날짜'] = df2['날짜'].str[0:6]
    df2['time'] = df2['time'].astype(int)
    sun2['일출'] = sun2['일출'].astype(int)
    sun2['날짜'] = sun2['날짜'].astype(int)
    df2['날짜'] = df2['날짜'].astype(int)
    # 일출전 t부터 일출후 t까지 시간 구분 모듈 
    for i in range(len(sun)):
            # sum데이터의 월과 df의 월이 같고  time<일출 -> 전날 밤
        mask=((sun2.loc[i]['일출']-t_diff*100) <= df2['time'])&(df2['time']<=(sun2.loc[i]['일출']+t_diff*100))&( sun2.loc[i]['날짜'] == df2['날짜'])
        df_return.loc[mask,'day_thour'] = ment
    df_return=df_return.replace(np.nan,'')
    
    return df_return
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
        return sum(data)/len(data)
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
    for i in range(len(kind)):
        if("주간" in kind[i]):
            kind_ND[i] = "주간"
        if("야간" in kind[i]):
            kind_ND[i] = "야간"
        if("일출부터정오" in kind[i]):
            kind_ND[i] = '일출부터정오'
        if(ment  in kind[i]):
            kind_ND[i] = ment      

    date_seq = data.iloc[:,date_ind].astype('str').apply(lambda x: x[0:10]).replace('-','',regex=True)
    date = pd.Series(pd.to_datetime(date_seq.unique(), format="%Y-%m-%d")) 
    # 만약 div_DN이 있을 시의 코드
    # if ("야간" in kind_ND):
    #     date = date.apply(lambda x: x - dt.timedelta(days=1))

    ary = np.empty(shape=(len(date),len(kind)*len(d_ind),))
    ary[:] = np.nan

    temp_df = pd.DataFrame(ary)

    ind_name = data.columns[d_ind].tolist()

    temp_name = []
    #temp_name<-vector(length=length(kind)*length(d_ind))
    for ind in ind_name:
        for k in kind:
            if type(k) == list :
                temp_name.append(k[0]+k[1]+" "+ind)
            else:
                temp_name.append(k+ " " + ind)

    temp_df.columns = temp_name
    #temp_df에 값 입력과정
    for i in range(len(date)):
        date_i = date.astype('str').replace('-','',regex=True)
        date_i2 = date_i[i]
        if ('전체' in kind_ND):
            today_ind = date_seq[ date_seq==date_i2 ].index.tolist()
        if ('주간' in kind_ND):
            daytime_ind = div_DN.index[(div_DN['div']=='주간') & (div_DN['날짜']==date_i2)].tolist()
        if ('야간' in kind_ND):
            night_ind = div_DN.index[(div_DN['div']=='야간') & (div_DN['날짜']== date_i2)].tolist()
        if ('일출부터정오' in kind_ND):
            noon_ind = div_DN.index[(div_DN['day_afternoon']=='일출부터정오') & (div_DN['날짜']==date_i2)].tolist()
        if (ment  in kind_ND):
            thour_ind = div_DN.index[(div_DN['day_thour']==ment ) & (div_DN['날짜']==date_i2)].tolist()
        for j in d_ind:
            for kind_num in range(len(kind)):
                if (kind_ND[kind_num] == "주간"):
                    if(data.iloc[daytime_ind,j].isna().sum()==0):
                        if(data.iloc[daytime_ind,j].empty == False):
                            temp_df.iloc[i,kind_num] = functions_list[list(functions_list.keys())[kind_div[kind_num]]](data.iloc[daytime_ind,j].tolist())
                elif (kind_ND[kind_num] == "야간"):
                    if(data.iloc[night_ind,j].isna().sum()==0):
                        if(data.iloc[night_ind,j].empty == False):
                            temp_df.iloc[i,kind_num] = functions_list[list(functions_list.keys())[kind_div[kind_num]]](data.iloc[night_ind,j].tolist())
                elif (kind_ND[kind_num] == "전체"):
                    if(data.iloc[today_ind,j].isna().sum()==0):
                        if(data.iloc[today_ind,j].empty == False):
                            temp_df.iloc[i,kind_num] = functions_list[list(functions_list.keys())[kind_div[kind_num]]](data.iloc[today_ind,j].tolist())
                elif (kind_ND[kind_num] == "일출부터정오"):
                    if(data.iloc[noon_ind,j].empty == False):
                        if(data.iloc[noon_ind,j].isna().sum()==0):
                            temp_df.iloc[i,kind_num] = functions_list[list(functions_list.keys())[kind_div[kind_num]]](data.iloc[noon_ind,j].tolist())
                elif (kind_ND[kind_num] == ment ):
                    if(data.iloc[thour_ind,j].empty == False):
                        if(data.iloc[thour_ind,j].isna().sum()==0):
                            temp_df.iloc[i,kind_num] = functions_list[list(functions_list.keys())[kind_div[kind_num]]](data.iloc[thour_ind,j].tolist())
    temp_df = pd.concat([pd.DataFrame(date, columns=['날짜']),temp_df], axis=1)      
    return temp_df

@logging_time
def generating_dailydata(df, date_ind, t_div, t_diff, var, elsewhere=None):

    ment = '일출전후'+ str(t_diff)+'시간'
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
        # h = generating_variable(df, date_ind, hum, ["평균",["주간","평균"], ["야간","평균"], "최소","최대"],t_diff, t_div)
        # c = generating_variable(df, date_ind, co2, ["평균","최대","최소",["일출부터정오","평균"]],t_diff,t_div)
        # s = generating_variable(df, date_ind, cumsolar, [["주간","최대"]],t_diff, t_div)
    
    
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
    date=gdata['날짜']
    lastDate=pd.to_datetime(date.iloc[-1])
    if type(date[0]) != str:
        date = date.astype('str')
    if type(date[0]) != type(pd.to_datetime(date)[0]):
        date = pd.to_datetime(date)
    if interval == 7 :
        print(date[0])
        weeknum = int(datetime.datetime(date[0].year,date[0].month,date[0].day).strftime("%U"))
        print(weeknum)
        date1 = pd.to_datetime(datetime.datetime.strptime(f"{date[0].year}-W{weeknum}-1", "%G-W%V-%u")) #해당 주차의 마지막 날짜
        print(date1)
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
            week.append(weeknum+1)
            i+=1
        weeknum+=1
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