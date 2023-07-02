
from django.shortcuts import render, redirect
from .models import File_db
from django.core.files import File
import pandas as pd
from users.models import User
import json
import os
from . import proc

from config.settings import BASE_DIR
from django.http import JsonResponse
from django.http import HttpResponse
#-----------------------DRF import-----------------------
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .serializers import FileSerializer, UserSerializer
#-----------------------유틸리티 import-----------------------
from .decorators import logging_time
from .validators import loginValidator
from .utils import FileSystem, DataProcess, cacheGetter
##페이지 별로 필요한 request를 컨트롤
#---------------분석도구 import ----------------
from . import analizer
#-----------------------메인화면 호출. user정보를 사용

def main(request):
    user = loginValidator(request)
    if user != None:
            context={'user_name':user.user_name}
            return render(request,'main/main.html',context)
    if user == None:
            return render(request,'main/main.html')

#------------------------ management창 ------------------------
def fileList(request):
    user = loginValidator(request)
    if user != None:
            file_object=File_db.objects.filter(user_id=user.id)
            context={'user_name':user.user_name,
                'files':file_object}
            return render(request,'fileList/fileList.html',context)
    elif user == None:
            return HttpResponse("<script>alert('올바르지 않은 접근입니다.\\n\\n이전 페이지로 돌아갑니다.');location.href='/';</script>")

#파일 업로드 함수 - data_list창
def fileUploadView(request):
    if request.method == 'POST':
        user = loginValidator(request)
        FileSystem(user).fileUpload(request)
        return redirect('/fileList/')
    elif request.method == 'GET':
        user = loginValidator(request)
        FileSystem(user).fileUpload(request)
        return render(request, 'upload/upload.html')

def fileDeleteView(request):
    user = loginValidator(request)
    result = FileSystem(user).fileDelete(request)
            # Redirect to a success page.
    return JsonResponse(result)

#파일 삭제 함수 - data_list창
    
#------------------------ revise창 ------------------------
@logging_time
def revise(request, file_name):
    user = loginValidator(request)
    if user != None:
        context = FileSystem(user).fileLoad(file_name)
        return render(request, "revise/revise.html", context) #전송
    else:
        return HttpResponse("<script>alert('올바르지 않은 접근입니다.\\n\\n이전 페이지로 돌아갑니다.');location.href='/';</script>")
    
def revise2(request):
    user = loginValidator(request)
    if user != None:
        context={'user_name':user.user_name}
        return render(request, "revise/revise.html", context)
    else:
        return HttpResponse("<script>alert('올바르지 않은 접근입니다.\\n\\n이전 페이지로 돌아갑니다.');location.href='/';</script>")
#--------------파일 정보 비동기 불러오기 - revise창-------------
def fileLoadView(request):
    user = loginValidator(request)
    context = FileSystem(user).fileLoad(request)
    return JsonResponse(context)

#------------------------ merge창 ------------------------
def merge(request):
    user = loginValidator(request)
    if user != None:
        context={'user_name':user.user_name}
        return render(request, "merge/merge.html", context) #전송
    else:
        return HttpResponse("<script>alert('올바르지 않은 접근입니다.\\n\\n이전 페이지로 돌아갑니다.');location.href='/';</script>")

def mergeView(request):
    user = loginValidator(request)
    if request.method == 'GET':
        files = request.GET.get('data')
        files = json.loads(files)
        context = FileSystem(user).fileLoadMulti(files)
        return JsonResponse(context)
    elif request.method == 'POST':
        if request.POST.get('header') == 'merge':
            data = pd.read_json(request.POST.get('data'))
            data1 = data.iloc[0,0]
            data2 = data.iloc[1,0]
            data1 = pd.read_json(data1) 
            data2 = pd.read_json(data2)
            var1, var2 = request.POST.get('var1'), request.POST.get('var2')
            mergeData = pd.merge(data1, data2, how='outer', left_on=var1, right_on=var2)
            mergeData = mergeData.to_json(orient='records', force_ascii=False)
            print(mergeData)
            return JsonResponse({'result':'success',
                                'data':mergeData})
        elif request.POST.get('header') == 'save':
            data = request.POST.get('data')
            print("-------------"+data)
            file_name = request.POST.get('file_name')
            data = pd.read_json(data)
            FileSystem(user).fileSave(data, file_name)
            return JsonResponse({'result':'success'})

#------------------------ analysis창 ------------------------
def fileList2(request):
    user = loginValidator(request)
    if user != None:
        file_object=File_db.objects.filter(user_id=user.id)
        context={'user_name':user.user_name,
            'files':file_object}
        return render(request, "fileList_2/fileList_2.html", context) #전송
    elif user == None:
        return HttpResponse("<script>alert('올바르지 않은 접근입니다.\\n\\n이전 페이지로 돌아갑니다.');location.href='/';</script>")

def analyze(request, file_name):
    user = loginValidator(request)
    if user != None:
        context = FileSystem(user).fileLoad(file_name)
        return render(request, "Analyze/analyze.html", context) #전송
    elif user == None:
        return HttpResponse("<script>alert('올바르지 않은 접근입니다.\\n\\n이전 페이지로 돌아갑니다.');location.href='/';</script>")

def useAnalizer(request, file_name):
    user = loginValidator(request)
    if user != None:
        if cacheGetter(user, file_name) == True:
            data = cacheGetter(user, file_name)
            data = pd.read_json(data)
        else:
            file_object=File_db.objects.get(user_id=user, file_Title=file_name)

            work_dir = './media/' + str(file_object.file_Root)
            if os.path.splitext(work_dir)[1] == ".csv":
                try:
                    data=pd.read_csv(work_dir,encoding="cp949")
                except UnicodeDecodeError:
                    data=pd.read_csv(work_dir,encoding="utf-8")
            else:
                data = pd.read_excel(work_dir, sheet_name= 0)

        if request.GET.get('technique') == "선형회귀분석":
            print("들어왔다")
            x = json.loads(request.GET.get('xValue'))
            y = request.GET.get('yValue')
            result = analizer.linear(data, x, y)
            print(x,y, result)
            return JsonResponse({'result':'success','data':result})
        # elif request.POST.get('header') == 'ttest':
        #     type = request.POST.get('type')
        #     if type == '2':
        #         x = request.POST.get('x_value')
        #         result = proc.ttest(data, type, x)
        #         return JsonResponse({'result':'success',
        #                             'data':result})
        #     elif type == '3':
        #         x = request.POST.get('x_value')
        #         y = request.POST.get('y_value')
        #         result = proc.ttest(data, type, x, y)
        #         return JsonResponse({'result':'success',
        #                             'data':result})
        #     elif type == '4':
        #         x = request.POST.get('x_value')
        #         y = request.POST.get('y_value')
        #         result = proc.ttest(data, type, x, y)
        #         return JsonResponse({'result':'success',
        #                             'data':result})
        elif request.GET.get('technique') == '선형회귀분석':
            x = request.POST.getlist('x_value')
            y = request.POST.get('y_value')
            result = analizer.logistic(data, x, y)
            return JsonResponse({'result':'success',
                                'data':result})
    elif user == None:
        return HttpResponse("<script>alert('올바르지 않은 접근입니다.\\n\\n이전 페이지로 돌아갑니다.');location.href='/';</script>")
#------------------------ test.html연결 ------------------------
def test(request):
    return render(request, "analytics/excel.html") #전송

#------------------------------농업관련 데이터 처리 부분------------------
#데이터의 형식이나 원하는 전처리에 따라 파이프라인을 설정하는 부분
@logging_time
def farm(request, file_name):
    user = loginValidator(request)
    new_file_name=request.POST.get('new_file_name')
    file_type=request.POST.get('file_type','환경')
    date=request.POST.get('date','1')
    lat=request.POST.get('lat','35')
    lon=request.POST.get('lon','126')
    lat_lon=[lat,lon]
    DorW=request.POST.get('DorW','days')
    var=request.POST.get('valueObject')
    var=json.loads(var)
    print(file_name)
    data=FileSystem(user).fileGetter(file_name)

    a = ETL_system(data,file_type,date,lat_lon,DorW,var)
    result=a.ETL_stream()
    FileSystem(user).fileSave(result, new_file_name)
    result_json=result.to_json(orient="records",force_ascii=False)
    result = {
                'result':'success',
                'data' : result_json,
            }
            # Redirect to a success page.
    return JsonResponse(result)




class ETL_system:
    def __init__(self,data,file_type,date,lat_lon,DorW,var):
        self.data = data
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
        print(self.data)
        df = DataProcess(self.data, self.date)
        df.dateConverter()
        if self.DorW=="weeks":
        #주별데이털로 변환
            result = proc.making_weekly2(df.data, df.date)
            result['날짜']=result['날짜'].astype('str')
        elif self.DorW == 'days':
            #시간 구별 데이터프레임 생성
            envir_date = pd.DataFrame()
            envir_date['날짜'] = df.getDate()

            start_month=envir_date['날짜'].astype(str)[0][0:7]
            end_month=envir_date['날짜'].astype(str)[len(envir_date)-1][0:7]
            sun = proc.get_sun(round(float(lon)),round(float(lat)),start_month,end_month)
            #낮밤구분
            nd_div=proc.ND_div(sun, envir_date)
            #정오구분
            afternoon_div =proc.afternoon_div(sun, nd_div, noon=12)
            #일출일몰t시간전후
            t_diff=3
            t_div=proc.time_div(sun,afternoon_div, t_diff)
            #일일데이터로 변환
            generating_data=proc.generating_dailydata(df.data, df.date, t_div,t_diff, self.var)
            result=generating_data
        else:
            result = proc.making_weekly2(df.data, df.date, int(self.DorW))
            result['날짜']=result['날짜'].astype('str')
        result['날짜']=result['날짜'].astype('str')
        return result
    
    #생육데이터 처리함수
    def Growth(self):
        print("--------------생육입니다.-------------------------")
        print(self.date)
        dt = DataProcess(self.data, self.date)
        dt.dateConverter()
        growth_object = dt.data
        date = dt.date
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
    

#------------------------ APIview ------------------------
@api_view(['GET'])
def userApiView(request):
    user = User.objects.all()
    serializer = UserSerializer(user, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def fileListApiView(request):
    fileList = File_db.objects.all()
    serializer = FileSerializer(fileList, many=True)
    return Response(serializer.data)




