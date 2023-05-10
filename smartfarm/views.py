
from django.shortcuts import render, redirect
from .models import File_db
from django.core.files import File
import pandas as pd
import copy
from users.models import User
import numpy as np
import json
from . import analizer, proc
from config.settings import BASE_DIR
from django.http import JsonResponse
import os
from django.utils.datastructures import MultiValueDictKeyError
from .decorators import logging_time

##페이지 별로 필요한 request를 컨트롤
#-----------------------메인화면 호출. user정보를 사용56
def main(request):
    id = request.session.get('user')#session데이터불러오기
    if id != None:
            user=User.objects.get(id=id)
            context={'user_name':user.user_name}
            return render(request,'main/main.html',context)
    if id == None:
            return render(request,'main/main.html')

#------------------------ management창 ------------------------
def manage(request):
    id = request.session.get('user')
    if id != None:
            user=User.objects.get(id=id)
            file_object=File_db.objects.filter(user_id=id)
            context={'user_name':user.user_name,
                'files':file_object}
            return render(request,'datamanage/manage.html',context)
    if id == None:
            return render(request,'datamanage/manage.html')

def merge(request):
    return render(request,'merge/merge.html')

#파일 업로드 함수 - manage창
@logging_time
def file_uploading(request):
    id = request.session.get('user')
    if request.method == 'POST':
        uploadedFile = request.FILES["file_input"]
        try:
            file_name=request.POST['upload_title']
        except MultiValueDictKeyError:
            file_name=str(uploadedFile)

        if File_db.objects.filter(user_id=id, file_Title=file_name):
            file_name_copy = copy.copy(file_name)
            unique = 1
            while File_db.objects.filter(user_id=id, file_Title=file_name_copy):
                unique+=1
                file_name_copy=file_name+"_"+str(unique)
            file_name = file_name_copy
        print("----------------------",uploadedFile)
        print(uploadedFile,type(uploadedFile))
        if uploadedFile != None:
            file_form =File_db(
                user_id=User.objects.get(id=id),
                file_Title=file_name,
                file_Root=uploadedFile,
            )
            file_form.save()
        return redirect("smartfarm:manage")
    
#------------------------ show창 ------------------------
def show(request,file_name):
    id = request.session.get('user')#접속한 유저데이터 획득
    file_object=File_db.objects.get(user_id=id,file_Title=file_name)#파일명을 유저기준으로 찾아서 변수로 저장
    fileList=File_db.objects.filter(user_id=id)
    work_dir = './media/' + str(file_object.file_Root)#저장된 경로에서 파일을 꺼내옴
    if os.path.splitext(work_dir)[1] == ".csv":#파일의 확장자를 검사
        try:
            data=pd.read_csv(work_dir,encoding="cp949")
        except UnicodeDecodeError:
            data=pd.read_csv(work_dir,encoding="utf-8")
    else:#excel일경우 read_excel아닐경우 read_csv
        data = pd.read_excel(work_dir, sheet_name = 0)
    data[data.select_dtypes(exclude=['object']).columns] = data.select_dtypes(exclude=['object']).round(decimals = 2)
    data[data.select_dtypes(include=['object','datetime64[ns]']).columns] = data.select_dtypes(include=['object','datetime64[ns]']).astype(str)
    #-------------열별 요약데이터 생성--------------
    summary = makeSummary(data)
    #----------------------------------------------
    data=data.replace({np.nan: 0})#결측치를 처리해줌
    data_json=data.to_json(orient="records",force_ascii=False)#데이터프레임을 json배열형식으로변환(형식은 spreadsheet.js에 맞춰)
    summary_json = summary.to_json(orient="columns",force_ascii=False)
    context = {#파일명과 파일데이터를 폼으로 저장
                'data' : data_json,
                'summarys' : json.loads(summary_json)
            }
    return render(request, "show/show.html", context) #전송

@logging_time
def makeSummary(df):
    nullCountData=pd.DataFrame(df.isnull().sum()).T
    # typeData=pd.DataFrame(data.dtypes).T
    # nullIndexData=data.apply(lambda x: x.index[x.isnull()].tolist()).T
    nullCountData.index=["Null_count"]
    # typeData.index=["types"]
    # nullIndexData.index=["nullIndex"]
    # typeData = typeData.astype("str")
    try:
        numData = df.describe().iloc[[4,5,6,1,3,7],:]
        numData.index = ["Q1","Q2","Q3","mean","min","max"]
        summary = pd.concat([nullCountData,numData], ignore_index=False)
        summary = summary.replace({np.nan: "-"})#결측치를 처리해줌
        summary = summary.round(2)
    except IndexError:
        numData = pd.DataFrame(index = ["Q1","Q2","Q3","mean","min","max"], columns = df.columns)
        summary = pd.concat([nullCountData,numData], ignore_index=False)
        summary = summary.replace({np.nan: "-"})#결측치를 처리해줌
    return summary

#------------------------업로드 및 저장관련 ------------------------


@logging_time
def fileDelete(request):
    id = request.session.get('user')
    files = request.POST.get('data')
    files = json.loads(files)
    for i in range(len(files)):
        file_object=File_db.objects.get(user_id=id,file_Title=files[i])
        file_object.delete()
        os.remove('./media/' + str(file_object.file_Root))
    result = {
                'result':'success'
            }
            # Redirect to a success page.
    return JsonResponse(result)

@logging_time
def fileSave(id, result,file_name):#결과 dataframe, object:파일경로
    #전처리 후 excel파일로 변환 > open()을 통해 이진형식 rb로 읽어야 db에 저장가능
    #---------------같은 이름 파일명 처리-------------
    if File_db.objects.filter(user_id=id, file_Title=file_name+".csv"):
        file_name_copy = copy.copy(file_name)
        unique = 1
        while File_db.objects.filter(user_id=id, file_Title=file_name_copy+".csv"):
            unique+=1
            file_name_copy=file_name+"_"+str(unique)
        file_name = file_name_copy+".csv"
        result.to_csv(file_name)
    else:
        file_name = file_name+".csv"
        result.to_csv(file_name)
    #--------------------------------------------------
    f = open(file_name,'rb')
    file_open=File(f,name=file_name)
    file_form = File_db(user_id=User.objects.get(id=id),file_Title=file_name,file_Root=file_open)
    file_form.save()
    f.close()
    os.remove(file_name)
    return 0


#--------------파일 정보 불러오기-------------

@logging_time
def load_data(request):
    id = request.session.get('user')#접속한 유저데이터 획득
    file_name=request.POST['file_name']
    print(file_name)
    file_object=File_db.objects.get(user_id=id, file_Title=file_name)
    work_dir = './media/' + str(file_object.file_Root)
    if os.path.splitext(work_dir)[1] == ".csv":
        try:
            data=pd.read_csv(work_dir,encoding="cp949")
        except UnicodeDecodeError:
            data=pd.read_csv(work_dir,encoding="utf-8")
    else:
        data = pd.read_excel(work_dir, sheet_name= 0)
    data[data.select_dtypes(exclude=['object']).columns] = data.select_dtypes(exclude=['object']).round(decimals = 2)
    data[data.select_dtypes(include=['object','datetime64[ns]']).columns] = data.select_dtypes(include=['object','datetime64[ns]']).astype(str)
    summary=makeSummary(data)
    #---------------json생성------------------
    data=data.replace({np.nan: 0})
    data_json=data.to_json(orient="records",force_ascii=False)#데이터프레임을 json배열형식으로변환(형식은 spreadsheet.js에 맞춰)
    summary_json = summary.to_json(orient="columns",force_ascii=False)
    context = {
                'result':'success',
                'data' : data_json,
                'summarys' : json.loads(summary_json)
            }
    return JsonResponse(context)

# #분석호출함수
# @logging_time
# def probing(request):
#     prob_type=request.POST.get("prob","")
#     data=request.POST['data']
#     if prob_type=="1":
#         result=analizer.linear(data)
#     elif prob_type=="2" or prob_type=="3" or prob_type=="4":
#         result=analizer.ttest(data)
#     elif prob_type=="5":
#         result=analizer.logistic(data)
        
#     context={"result":result}
#     return render(request,'analytics/anal_result.html',context)

#------------------마이페이지 관련 ----------------------
def mypage(request):
    id = request.session.get('user')
    file_root=File_db.objects.filter(user_id=id)
    print(file_root)
    context={"file":file_root, }
    return render(request, "mypage/mypage.html",context)


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
    # if file_type == '합치기':
    #     data=request.POST.getlist('data')
    #     result = ETL_system.join_data(data)
    #     result_json=result.to_json(orient="records",force_ascii=False)
    #     result = {
    #             'result':'success',
    #             'data' : result_json,
    #         }
    #         # Redirect to a success page.
    #     return JsonResponse(result)
        
    a = ETL_system(data,file_type,date,lat_lon,DorW,var)
    result=a.ETL_stream()
    fileSave(id, result, file_name)
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
    




