
from django.shortcuts import render, redirect
from .models import File_db
from django.core.files import File
import pandas as pd
import copy
from users.models import User
import numpy as np
import json
from . import proc
from config.settings import BASE_DIR
from django.http import JsonResponse
import os
from django.utils.datastructures import MultiValueDictKeyError
#-----------------------유틸리티 import-----------------------
from .decorators import logging_time
from .validators import loginValidator
from .utils import FileSystem, DataProcess
##페이지 별로 필요한 request를 컨트롤

#-----------------------메인화면 호출. user정보를 사용56
def main(request):
    user = loginValidator(request)
    if user != None:
            context={'user_name':user.user_name}
            return render(request,'main/main.html',context)
    if user == None:
            return render(request,'main/main.html')

#------------------------ management창 ------------------------
def manage(request):
    user = loginValidator(request)
    if user != None:
            file_object=File_db.objects.filter(user_id=user.id)
            context={'user_name':user.user_name,
                'files':file_object}
            return render(request,'datamanage/manage.html',context)
    if user == None:
            return render(request,'datamanage/manage.html')

def merge(request):
    return render(request,'merge/merge.html')

#파일 업로드 함수 - manage창
def fileUploadView(request):
    user = loginValidator(request)
    FileSystem(user).fileUpload(request)
    return redirect("smartfarm:manage")

def fileDeleteView(request):
    user = loginValidator(request)
    result = FileSystem(user).fileDelete(request)
            # Redirect to a success page.
    return JsonResponse(result)

#파일 삭제 함수 - manage창
    
#------------------------ show창 ------------------------
def show(request):
    user = loginValidator(request)
    context = FileSystem(user).fileLoad(request)
    return render(request, "show/show.html", context) #전송

#--------------파일 정보 비동기 불러오기 - show창-------------
def fileLoadView(request):
    user = loginValidator(request)
    context = FileSystem(user).fileLoad(request)
    return JsonResponse(context)


#------------------------------농업관련 데이터 처리 부분------------------
#데이터의 형식이나 원하는 전처리에 따라 파이프라인을 설정하는 부분
@logging_time
def farm(request):
    id = request.session.get('user')
    file_name=request.POST.get('file_name')
    file_type=request.POST.get('file_type','기본')
    date=request.POST.get('date','0')
    lat=request.POST.get('lat','35')
    lon=request.POST.get('lon','126')
    lat_lon=[lat,lon]
    DorW=request.POST.get('DorW','days')
    var=request.POST.get('valueObject')
    var=json.loads(var)
    data=request.POST['data']
    print(var)
        
    a = ETL_system(data,file_type,date,lat_lon,DorW,var)
    result=a.ETL_stream()
    FileSystem.fileSaveForm(id, result, file_name)
    result_json=result.to_json(orient="records",force_ascii=False)
    result = {
                'result':'success',
                'data' : result_json,
            }
            # Redirect to a success page.
    return JsonResponse(result)




class ETL_system:
    def __init__(self,data,file_type,date,lat_lon,DorW,var):
        b=pd.read_json(data)
        self.data = b
        self.file_type = file_type
        self.date = int(date) - 1
        self.lat, self.lon=lat_lon
        self.DorW = DorW
        self.var = var

    def ETL_stream(self):
        if self.file_type == '환경':
            after_d=self.Envir()
        if self.file_type == '생육':
            after_d=self.Growth()
        if self.file_type == '생산량':
            after_d=self.Crop()
        return after_d
    
    #객체로 들어온 파일을 업데이트하여 저장    

    #환경데이터 처리함수
    def Envir(self):
        lon = self.lon
        lat = self.lat
        date = self.date #날짜가 포함된 열.
        if(self.DorW=="weeks"):
        #주별데이털로 변환
            result = proc.making_weekly2(self.data, date)
            result['날짜']=result['날짜'].astype('str')
        elif self.DorW == 'days':
            #시간 구별 데이터프레임 생성
            envir_date = pd.DataFrame()
            envir_date['일시'] = self.data.iloc[:,date].to_list()
            if type(envir_date['일시'][0]) != str:
                self.data.iloc[:,date] = self.data.iloc[:,date].astype(str)
                self.data.iloc[:,date] = pd.to_datetime(self.data.iloc[:,date]).astype(str)
                envir_date['일시'] = envir_date['일시'].astype(str)
            envir_date['일시'] = pd.to_datetime(envir_date['일시']).astype(str)
            print(envir_date['일시'][0])
            # [long,lati]=proc.geocoding(address)
            start_month=str(pd.to_datetime(envir_date['일시'].iloc[0]))[0:7]
            end_month=str(pd.to_datetime(envir_date['일시'].iloc[-1]))[0:7]
            #일출일몰
            sun = proc.get_sun(round(float(lon)),round(float(lat)),start_month,end_month)
            #낮밤구분
            nd_div=proc.ND_div(sun, envir_date)
            #정오구분
            afternoon_div =proc.afternoon_div(sun,nd_div,noon=12)
            #일출일몰t시간전후
            t_diff=3
            t_div=proc.time_div(sun,afternoon_div, t_diff)
            t_div['일시']=t_div['일시'].astype('str')
            #일일데이터로 변환
            generating_data=proc.generating_dailydata(self.data, date, t_div,t_diff, self.var)
            result=generating_data
        else:
            result = proc.making_weekly2(self.data, date, int(self.DorW))
            result['날짜']=result['날짜'].astype('str')
        result['날짜']=result['날짜'].astype('str')
        return result
    
    #생육데이터 처리함수
    def Growth(self):
        growth_object = self.data
        date = self.date
        date = int(date)
        result=proc.making_weekly2(growth_object,date)
        result['날짜']=result['날짜'].astype('str')
        return result

    #생산량데이터 처리함수
    def Crop(self):
        crop=self.data
        date_ind=self.date
        d_ind=1
        result=proc.y_split(crop,date_ind,d_ind)
        result['날짜']=result['날짜'].astype('str')
        return result
    
    #weekly함수 실행 시에 날짜의 열이름이 '날짜'로 통일되는 점을 활용, 주별데이터, 중복없는 일일데이터 가능
    def join_data(x):
        env,prod,yld=x[0],x[1],x[2]
        env_prod=pd.merge(env,prod,left_on="날짜",right_on="날짜",how="outer")
        env_prod_yld=pd.merge(env_prod,yld,left_on="날짜",right_on="날짜",how="outer")
        print(env_prod_yld)
        return env_prod_yld
    




