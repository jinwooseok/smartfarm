
from django.shortcuts import render, redirect
import pandas as pd
import json
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from django.http import JsonResponse
from django.http import HttpResponse
from django.http import FileResponse
#-----------------------DRF import-----------------------
from .response import *
from .repositorys import *
#-----------------------유틸리티 import-----------------------
from .decorators import logging_time
from .validators import loginValidator
from .utils.FileSystem import FileSystem
from .utils.DataProcess import DataProcess
from .proc import ETL_system
import os
from django.conf import settings

##페이지 별로 필요한 request를 컨트롤
#---------------분석도구 import ----------------
from . import analizer

from django.utils.datastructures import MultiValueDictKeyError


def main(request):
    user = loginValidator(request)
    if user is None:
            return render(request,'Html/main.html')
    else:
        context={'user_name':user.user_name}
        return render(request,'Html/main.html',context)

#------------------------ management창 ------------------------
def fileListView(request):
    user = loginValidator(request)
    if user is None:
        return HttpResponse("<script>alert('올바르지 않은 접근입니다.\\n\\n이전 페이지로 돌아갑니다.');location.href='/';</script>")
    
    file_object=findFileObjectListByUserId(user.id)
    
    context=fileListViewResponse(user.user_name, file_object)

    return render(request,'Html/fileList.html',context)

#파일 업로드 함수 - data_list창
def fileUploadApi(request):
    user = loginValidator(request)
    try:
        file_title = request.POST.get('file_title')
    except MultiValueDictKeyError:
        return JsonResponse(failResponse("파일명을 선택해주세요."), status=400)
    try:
        file = request.FILES["fileUploadInput"]
    except MultiValueDictKeyError:
        try:
            file = request.FILES["fileUploadDrag"]
        except MultiValueDictKeyError:
            return JsonResponse(failResponse("파일명을 선택해주세요."), status=400)
    FileSystem(user=user,file_title=file_title,multi_part_file=file).fileUpload()
    
    return redirect('/file-list/')

    
#파일 삭제 함수 - data_list창
def fileDeleteApi(request):
    user = loginValidator(request)
    try:
        file_titles = request.POST.get('data')
    except MultiValueDictKeyError:
        return JsonResponse(failResponse("파일명을 선택해주세요."), status=400)
    for file_title in json.loads(file_titles):
        FileSystem(user=user,file_title=file_title).fileDelete()
    #response
    context = successResponse()
    return JsonResponse(context)

#파일 다운로드 함수
def fileDownloadApi(request):
    user = loginValidator(request)

    try:
        file_title = request.POST.get('data')
    except MultiValueDictKeyError:
        return JsonResponse(failResponse("파일명을 선택해주세요."), status=400)
    #파일의 데이터
    result = FileSystem(user=user,file_title=file_title).fileLoad()

    context = fileDownLoadApiResponse(file_title, result)

    return JsonResponse(context)

#------------------------ revise창 ------------------------
@logging_time
def dataEditView(request, file_title):
    user = loginValidator(request)
    if user is None:
        return HttpResponse("<script>alert('올바르지 않은 접근입니다.\\n\\n이전 페이지로 돌아갑니다.');location.href='/';</script>")
    
    file_title_list = findFileObjectListByUserId(user.id).values_list('file_title', flat=True)
    data = FileSystem(user=user, file_title=file_title).fileLoad()
    summary = DataProcess(data).makeSummary()
    #response dto
    context = dataEditViewResponse(data, summary, user.user_name, file_title_list)
    return render(request, "Html/revise.html", context) #전송

    
def dataEditWithNoFileView(request):
    user = loginValidator(request)
    if user is None:
        return HttpResponse("<script>alert('올바르지 않은 접근입니다.\\n\\n이전 페이지로 돌아갑니다.');location.href='/';</script>")
        
    context=dataEditWithNoFileViewResponse(user.user_name)
    
    return render(request, "Html/revise.html", context)

#--------------비동기 - revise창-------------
def dataLoadApi(request):
    user = loginValidator(request)
    if user is None:
        return JsonResponse(failResponse("로그인을 해주세요"), status=403)
    try:
        file_title = request.POST.get('fileName')
    except:
        return JsonResponse(failResponse("파일명을 선택해주세요."), status=400)
    data = FileSystem(user=user, file_title=file_title).fileLoad()

    summary = DataProcess(data).makeSummary()
    #response dto
    context = dataLoadApiResponse(data, summary, user.user_name)
    return JsonResponse(context)


def preprocessorApi(request, file_title):
    user = loginValidator(request)
    try:
        new_file_title = request.POST.get('newFileName')
    except:
        return JsonResponse(failResponse("파일명을 선택해주세요."), status=400)
    data = FileSystem(user=user,file_title=file_title).fileLoad()
    result = DataProcess(data).outLierDropper()
    
    FileSystem(user,file_title=new_file_title,data=result).fileSave()

    context = successDataResponse(result)

    return JsonResponse(context)

def abms_growth_api(request, file_title):
    user = loginValidator(request)
    try:
        data = request.POST.get('ABMSData')
    except:
        JsonResponse(failResponse("데이터를 선택해주세요."), status=400)
    try:
        new_file_title = request.POST.get('newFileName')
    except:
        return JsonResponse(failResponse("파일명을 선택해주세요."), status=400)
    if not data:
        print(data)
        return JsonResponse(failResponse("저장할 데이터가 비어있습니다."), status=400)
    FileSystem(user,file_title=new_file_title,data=data).fileSave()
    return JsonResponse(successResponse())

def abms_env_api(request, file_title):
    user = loginValidator(request)
    try:
        file_title = request.POST.get('fileName')
    except:
        return JsonResponse(failResponse("파일명을 선택해주세요."), status=400)
    date = request.POST.get('date','0')
    data = FileSystem(user=user, file_title=file_title).fileLoad()
    df = DataProcess(data,date)
    #날짜열을 날짜형식으로 변환
    df.dateConverter()
    #분단위라면 시간별로 변환. mask를 사용
    if df.isMinute():
        dateSeries = df.getDateSeries()
    #주간과 야간으로 변환
    return 0

#------------------------ merge창 ------------------------
def fileMergeView(request):
    user = loginValidator(request)
    file_list = FileSystem(user=user).getFileObjectList()
    if user != None:
        context=fileMergeViewResponse(user.user_name, file_list)
        return render(request, "Html/merge.html", context) #전송
    else:
        return HttpResponse("<script>alert('올바르지 않은 접근입니다.\\n\\n이전 페이지로 돌아갑니다.');location.href='/';</script>")

def fileMergeApi(request):
    user = loginValidator(request)
    if request.method == 'GET':
        file_name_list = FileSystem(user=user).getFileObjectList()
        if request.GET.get('data') == None:
            context = fileMergeApiResponse(file_name_list)
            return JsonResponse(context)
        else:
            try:
                files = request.GET.get('data')
            except:
                return JsonResponse(failResponse("데이터를 선택해주세요."), status=400)
            files = json.loads(files)
            data_list = []
            for file_title in files:
                data_list.append(FileSystem(user,file_title=file_title).fileLoad())

            context = fileMergeApiResponse(file_name_list, data_list)
            return JsonResponse(context)
        
    elif request.method == 'POST':
        if request.POST.get('header') == 'merge':
           #파일데이터 불러오기
            try:
                data = request.POST.get('data')
            except:
                return JsonResponse(failResponse("데이터를 선택해주세요."), status=400)
            try:
                column_name = request.POST.get('columnName')
            except:
                return JsonResponse(failResponse("기준 열을 입력해주세요."), status=400)
            dfs = []
            data = pd.read_json(data)
            column_name = json.loads(column_name)
            for i in range(len(data)):
                df = pd.read_json(data.iloc[i,0])
                df.rename(columns={column_name[i]:"기준"}, inplace=True)
                if type(df['기준']) is not object:
                    df['기준'] = df['기준'].astype(str)
                dfs.append(df)
            #data의 메모리 삭제
            del(data)

            merge_data = dfs[0]
        
            for i in range(1, len(dfs)):
                merge_data.info(memory_usage=True)
                dfs[i].info(memory_usage=True)
                merge_data = pd.merge(merge_data, dfs[i], on='기준', suffixes=(f'_{i}', f'_{i+1}'), how='outer', sort=True)
                print(merge_data)
            merge_json_objects = merge_data.apply(lambda row: json.loads(row.to_json(force_ascii=False)), axis=1).tolist()
            merge_json_string =  json.dumps(merge_json_objects)
            context = successDataResponse(merge_json_string)
            return JsonResponse(context)
        
        elif request.POST.get('header') == 'save':
            try:
                data = request.POST.get('mergedData')
            except:
                return HttpResponse("<script>alert('데이터를 선택해주세요');location.href='..';</script>")
            try:
                file_title = request.POST.get('fileName')
            except:
                return HttpResponse("<script>alert('파일명을 선택해주세요');location.href='..';</script>")
            FileSystem(user,file_title=file_title,data=data).fileSave()
            return JsonResponse(successResponse())
        else:
            return JsonResponse(failResponse("잘못된 입력입니다."), status=400)

def scalerApi(request, file_title):
    user = loginValidator(request)
    if user is None:
        return JsonResponse(failResponse("로그인을 해주세요"), status=403)
    
    file = FileSystem(user,file_title=file_title).fileLoad()
    data = pd.read_json(file)
    method = request.POST.get('method')

    if method == 'minmax':
        scaler = MinMaxScaler()
    
    if method =='standard':
        scaler = StandardScaler()
        
    scaled_data = scaler.fit_transform(data)
    scaled_data = scaled_data.to_json(orient='records', force_ascii=False)
    return JsonResponse(successDataResponse(scaled_data))

#------------------------ analysis창 ------------------------
def fileList2(request):
    user = loginValidator(request)
    if user is None:
        return HttpResponse("<script>alert('올바르지 않은 접근입니다.\\n\\n이전 페이지로 돌아갑니다.');location.href='/';</script>")
    
    file_object=findFileObjectListByUserId(user.id)
    
    context=fileListViewResponse(user.user_name, file_object)
    return render(request, "Html/fileList_2.html", context) #전송
    
def getAnalyzeDataApi(request, file_title):
    user = loginValidator(request)
    if user != None:
        result = FileSystem(user, file_title=file_title).fileLoad()
        context = analysisViewResponse(user.user_name,result)
        return render(request, "Html/analyze.html", context) #전송
    elif user == None:
        return HttpResponse("<script>alert('올바르지 않은 접근입니다.\\n\\n이전 페이지로 돌아갑니다.');location.href='/';</script>")

def useAnalizer(request, file_title):
    user = loginValidator(request)
    if user != None:
        data = FileSystem(user, file_title=file_title).fileLoad()
        data = pd.read_json(data)
        for i in data.columns:
            data[i] = pd.to_numeric(data[i], errors='coerce').astype(float)
        try:
            scaler = request.GET.get('scaler')
        except:
            return JsonResponse(failResponse("정규화 방식을 선택해주세요."), status=400)
        if scaler == 'min-max':
            scaler = MinMaxScaler()
            numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns
            data[numeric_columns] = scaler.fit_transform(data[numeric_columns])
            
        if scaler =='standard':
            scaler = StandardScaler()
            numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns
            data[numeric_columns] = scaler.fit_transform(data[numeric_columns])

        if scaler == 'notUse':
            pass    
        
        if request.GET.get('technique') == "선형회귀분석":
            try:
                x = json.loads(request.GET.get('xValue'))
                y = request.GET.get('yValue')
            except:
                return JsonResponse(failResponse("잘못된 x값 혹은 y값 입니다."), status=400)
            result = analizer.linear(data, x, y)
            if result == 400:
                return JsonResponse(failResponse("숫자가 아닌 잘못된 열이거나 값이 없습니다."), status=400)
            return JsonResponse(successDataResponse(result))

        elif request.GET.get('technique') == '로지스틱회귀분석':
            try:
                x = json.loads(request.GET.get('xValue'))
                y = request.GET.get('yValue')
            except:
                return JsonResponse(failResponse("잘못된 x값 혹은 y값 입니다."), status=400)
            result = analizer.logistic(data, x, y)
            if result == 400:
                return JsonResponse(failResponse("숫자가 아닌 잘못된 열이거나 값이 없습니다."), status=400)
            return JsonResponse(successDataResponse(result))
    elif user == None:
        return HttpResponse("<script>alert('올바르지 않은 접근입니다.\\n\\n이전 페이지로 돌아갑니다.');location.href='/';</script>")
#------------------------ test.html연결 ------------------------
def test(request):
    return render(request, "Html/excel.html") #전송

#------------------------------농업관련 데이터 처리 부분------------------
#데이터의 형식이나 원하는 전처리에 따라 파이프라인을 설정하는 부분
@logging_time
def farm(request, file_title):
    user = loginValidator(request)
    try:
        new_file_title=request.POST.get('new_file_name')
        file_type=request.POST.get('file_type','환경')
        date=request.POST.get('date','1')
        lat=request.POST.get('lat','35')
        lon=request.POST.get('lon','126')
        lat_lon=[lat,lon]
        DorW=request.POST.get('DorW','days')
        var=request.POST.get('valueObject')
        var=json.loads(var)
        startIndex = request.POST.get('startIndex', "1")
    except:
        return JsonResponse(failResponse("필수 입력값을 입력해주세요."), status=400)
    data=FileSystem(user,file_title=file_title).fileLoad()

    a = ETL_system(data,file_type,date,lat_lon,DorW,var,startIndex)

    result=a.ETL_stream()

    result_json=result.to_json(orient="records",force_ascii=False)
    
    FileSystem(user,file_title=new_file_title,data=result_json).fileSave()
            # Redirect to a success page.
    return JsonResponse(successDataResponse(result_json))


def guideBookDownloadApi(request):
    file_name = 'smartfarm_guidebook.pdf'
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)

    content_types = {
        "zip": "application/zip",
        "jpeg": "image/jpeg",
        "jpg": "image/jpeg",
        "pdf": "application/pdf",
        "ppt": "application/vnd.ms-powerpoint",
        "xls": "application/vnd.ms-excel",
        "7z": "application/x-7z-compressed",
        "gif": "image/gif",
        "others": "application/octet-stream"
    }
    c = content_types["others"]
    if file_name.split(".")[1] in content_types:
        c = content_types[file_name.split(".")[1]]

    if os.path.exists(file_path):
         with open(file_path, 'rb') as file:
            response = HttpResponse(file.read())
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(file_name)
            return response
    else:
        return JsonResponse(failResponse("파일을 찾을 수 없습니다."), status=400)

#def dataShift(request):
