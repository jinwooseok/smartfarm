
from django.shortcuts import render, redirect
from .models import File_db
from django.core.files.storage import Storage
from django.core.files import File
import pandas as pd
import sqlite3
from users.models import User
from django.views import View
import numpy as np
import json
from . import analizer,prep,proc
from config.settings import BASE_DIR
from django.http import JsonResponse
import os
from django.core.files.storage import FileSystemStorage

#메인화면 호출. user정보를 사용
def main(request):
    id = request.session.get('user')#session데이터불러오기
    if id != None:
            user=User.objects.get(id=id)
            context={'user_name':user.user_name}
            return render(request,'main/main.html',context)
    if id == None:
            return render(request,'main/main.html')



#------------------------업로드 및 저장관련 ------------------------
#파일 업로드 함수
def file_uploading(request):
    id = request.session.get('user')
    if request.method == 'POST':
        file_type=request.POST['f_type']
        uploadedFile = request.FILES["file"]
        file_name=str(uploadedFile).rsplit('.')[0]
        filetitle=file_name+'_'+file_type
        print("----------------------",uploadedFile)
        print(uploadedFile,type(uploadedFile))
        if uploadedFile != None:
            file_form =File_db(
                user_id=User.objects.get(id=id),
                file_Title=filetitle,
                file_Root=uploadedFile,
                file_type=file_type,
            )
            file_form.save()
        return redirect("smartfarm:mypage")
        

def fileSave(result,object):
    #전처리 후 excel파일로 변환 > open()을 통해 이진형식 rb로 읽어야 db에 저장가능
    file_name=str(object).rsplit('.')[0]
    after_name=file_name+'_after'
    after_File=result.to_excel(after_name+'.xlsx')
    f = open(after_File,'rb')
    file_open=File(f,name=str(after_File))
    file_form = File_db(user_id=User.objects.get(id=id),file_Title=after_name,after_file=file_open)
    file_form.save()
    return 0

#환경데이터 처리
# def Envir(request):
#     id = request.session.get('user')
#     file_object=File_db.objects.get(id=id)
#     work_dir = './media/' + str(file_object.file_Root)  # 저장 파일 위치 정보
#     envir = pd.read_csv(work_dir, encoding='cp949')
#     address='광주광역시'
#     # print(str(file_root.before_file))
#     # address='광주광역시'
#     # envir = pd.read_csv(work_dir+str(file_root.before_file), encoding='cp949')
#     envir_date = pd.DataFrame()
#     envir_date['일시'] = envir.iloc[:,0].to_list()
#     [long,lati]=proc.geocoding(address)
#     start_month=envir_date.iloc[0,0][0:7]
#     end_month=envir_date.iloc[-1,0][0:7]
#     #일출일몰
#     sun = proc.get_sun(round(long),round(lati),start_month,end_month)
#     #낮밤구분
#     nd_div=proc.ND_div(sun, envir_date)
#     #정오구분
#     afternoon_div =proc.afternoon_div(sun,nd_div,noon=12)
#     #일출일몰t시간전후
#     t_diff=3
#     t_div=proc.time_div(sun,afternoon_div, t_diff)
#     t_div['일시']=t_div['일시'].astype('str')
#     #일일데이터로 변환
#     generating_data=proc.generating_dailydata(envir, 0, t_div,t_diff,[3],[4],[5],[2],[6,7,9])
#     if(request.GET['DorW']=="week"):
#     #주별데이털로 변환
#         result = proc.making_weekly2(generating_data,0)
#         result['날짜']=result['날짜'].astype('str')
#         print(result)
#     #after저장
#     else:
#         result=generating_data
#         result['날짜']=result['날짜'].astype('str')
#     fileSave(result,file_object)
    # #json 배열형식으로 변경
    # result=result.replace({np.nan: 0})
    # result_json=result.to_json(orient="records",force_ascii=False)
    # return render(request,'analytics/index.html',context={"result_json":result_json,
    # })
    # return render(request,'analytics/index.html',{'result_json':result_json})
    #결과값 json파일로 변환

# Create your views here.



#생육데이터 처리
# def Growth(request):
#     id = request.session.get('user')
#     file_object=File_db.objects.get(id=id)
#     work_dir = './media/' + str(file_object.file_Root)  # 저장 파일 위치 정보
#     growth_object = pd.read_csv(work_dir, encoding='cp949')
#     result=proc.making_weekly2(growth_object,1)
#     fileSave(result,file_object)
    


#생산량데이터 처리
# def Crop(request):
#     id = request.session.get('user')
#     date_ind = request.GET['date_ind']
#     d_ind = request.GET['d_ind']
#     file_object=File_db.objects.get(id=id)
#     work_dir = './media/' + str(file_object.file_Root)  # 저장 파일 위치 정보
#     crop = pd.read_csv(work_dir, encoding='cp949')
#     #생산량 분할 모듈
#     #df:생산량 데이터 프레임
#     #date_ind:날짜 데이터 열
#     #d_ind:생산량 데이터 열
#     result=proc.y_split(crop,date_ind,d_ind)
#     fileSave(result,file_object)
    

#-------------excel창 관련------------------------
#작업창 호출함수
def excel(request):
    id = request.session.get('user')
    if id == None:
        return render(request,'analytics/excel.html')
    file_object=File_db.objects.filter(user_id=id)
    context={'files':file_object}
    return render(request,'analytics/excel.html',context)

#--------------파일 정보 불러오기-------------
def Summary(data):
    summary = {"null_list":[int(data[str(i)].isnull().sum()) for i in data.columns],
    "nrow":[int(len(data[str(i)])) for i in data.columns],
    "dtype":[str(data.dtypes[i]) for i in range(len(data.columns))],
    "cname":[str(i) for i in data.columns],
    }
    result=json.dumps(summary)
    return result

def load_data(request):
    filename=request.POST['filename']
    file_object=File_db.objects.get(file_Title=filename)
    work_dir = './media/' + str(file_object.file_Root)
    if os.path.splitext(work_dir)[1] == ".csv":
        data=pd.read_csv(work_dir,encoding="cp949")
    else:
        data = pd.read_excel(work_dir, sheet_name= 0)
    result=data.replace({np.nan: 0})
    summary=Summary(data)
    result_json=result.to_json(orient="records",force_ascii=False)
    result = {
                'result':'success',
                'data' : result_json,
                'summary' : summary,
            }
            # Redirect to a success page.
    return JsonResponse(result)
#분석호출함수
def probing(request):
    prob_type=request.POST.get("prob","")
    if prob_type=="1":
        result=analizer.lr_model(request)
        context={'result':result}
    elif prob_type=="2" or prob_type=="3" or prob_type=="4":
        result=analizer.t_test(request,prob_type)
        context={"result":result}
    elif prob_type=="5":
        result=analizer.logistic_test(request)
    return render(request,'analytics/anal_result.html',context)

#전처리관련





# def del_file(request):
#     request.POST.get('edit_file')
#     File_db.object.get('edit_file').delete()
#     return render(request, 'mypage/mypage.html')


#------------------마이페이지 관련 ----------------------
def mypage(request):
    id = request.session.get('user')
    file_root=File_db.objects.filter(user_id=id)
    print(file_root)
    context={"file":file_root, }
    return render(request, "mypage/mypage.html",context)

def farm(request):
    data=request.POST['jsonObject']
    file_type=request.POST['file_type']
    date=request.POST.get('date','0')
    address=request.POST.get('address','광주광역시')
    DorW=request.POST['DorW']
    a = ETL_system(data,file_type,date,address,DorW)
    result=a.ETL_stream()
    result_json=result.to_json(orient="records",force_ascii=False)
    result = {
                'result':'success',
                'data' : result_json,
            }
            # Redirect to a success page.
    return JsonResponse(result)
#------------------------------농업관련 데이터 처리 부분------------------
#데이터의 형식이나 원하는 전처리에 따라 파이프라인을 설정하는 부분
class ETL_system:
    def __init__(self,data,file_type,date,address,DorW):
        b=pd.read_json(data)
        self.data = b
        self.file_type = file_type
        self.date = date
        self.address=address
        self.DorW = DorW
    #객체의 file의 형식에 따라 관련 url로 이동
    # def ETL_stream(self,request):
    #     if request.POST['file_type'] == '환경':
    #         after_d=self.Envir()
    #     if request.POST['file_type'] == '생육':
    #         after_d=self.Growth()
    #     if request.POST['file_type'] == '생산량':
    #         after_d=self.Crop()
    #     return after_d

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
        # id = request.session.get('user')
        # file_object=File_db.objects.get(id=id)
        # work_dir = './media/' + str(file_object.file_Root)  # 저장 파일 위치 정보
        # envir = pd.read_csv(work_dir, encoding='cp949')
        date = self.date
        date = int(date)
        address='광주광역시'
        # envir = pd.read_csv(work_dir+str(file_root.before_file), encoding='cp949')
        envir_date = pd.DataFrame()
        envir_date['일시'] = self.data.iloc[:,date].to_list()
        [long,lati]=proc.geocoding(address)
        start_month=envir_date.iloc[0,0][0:7]
        end_month=envir_date.iloc[-1,0][0:7]
        #일출일몰
        sun = proc.get_sun(round(long),round(lati),start_month,end_month)
        #낮밤구분
        nd_div=proc.ND_div(sun, envir_date)
        #정오구분
        afternoon_div =proc.afternoon_div(sun,nd_div,noon=12)
        #일출일몰t시간전후
        t_diff=3
        t_div=proc.time_div(sun,afternoon_div, t_diff)
        t_div['일시']=t_div['일시'].astype('str')
        #일일데이터로 변환
        generating_data=proc.generating_dailydata(self.data, date, t_div,t_diff,[3],[4],[5],[2],[6,7,9])
        if(self.DorW=="week"):
        #주별데이털로 변환
            result = proc.making_weekly2(generating_data,date)
            result['날짜']=result['날짜'].astype('str')
            print(result)
        #after저장
        else:
            result=generating_data
            result['날짜']=result['날짜'].astype('str')
        return result
    
    #생육데이터 처리함수
    def Growth(self):
        # id = request.session.get('user')
        # file_object=File_db.objects.get(id=id)
        # work_dir = './media/' + str(file_object.file_Root)  # 저장 파일 위치 정보
        # growth_object = pd.read_csv(work_dir, encoding='cp949')
        growth_object = self.data
        date = self.date
        date = int(date)
        result=proc.making_weekly2(growth_object,date)
        return result

    #생산량데이터 처리함수
    def Crop(self):
        # id = request.session.get('user')
        # date_ind = request.GET['date_ind']
        # d_ind = request.GET['d_ind']
        crop=self.data
        date_ind=self.date
        d_ind=1
        # file_object=File_db.objects.get(id=id)
        # work_dir = './media/' + str(file_object.file_Root)  # 저장 파일 위치 정보
        # crop = pd.read_csv(work_dir, encoding='cp949')
        #생산량 분할 모듈
        #df:생산량 데이터 프레임
        #date_ind:날짜 데이터 열
        #d_ind:생산량 데이터 열
        result=proc.y_split(crop,date_ind,d_ind)
        return result
    
    #weekly함수 실행 시에 날짜의 열이름이 '날짜'로 통일되는 점을 활용, 주별데이터, 중복없는 일일데이터 가능
    def join_data(env,prod,yld):
        if len(env['날짜']) == len(prod['날짜']) == len(yld['날짜']):
            env_prod=pd.merge(env,prod)
            env_prod_yld=pd.merge(env_prod,yld)
            return env_prod_yld