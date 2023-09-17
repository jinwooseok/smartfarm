from .decorators import logging_time
import pandas as pd
import numpy as np
import os
import copy
import json

#---------------모델 import---------------------
from .models import File_db
#---------------오류 import---------------------
from django.utils.datastructures import MultiValueDictKeyError
## -------------파일 처리 클래스-----------------
from django.core.files import File
#--------------캐시 처리 라이브러리-------------
from django.core.cache import cache
class FileSystem:
    #백엔드에서 파일처리
    def __init__(self, user):
        self.user = user

    def getFileList(self):
        fileList=File_db.objects.filter(user_id=self.user)
        return fileList
    
    #파일 업로드 함수 - 처음 파일을 등록하는 함수
    def fileUpload(self, request):
        uploadedFile = request.FILES["file_input"]
        try:
            file_name=request.POST['upload_title']
        except MultiValueDictKeyError:#파일 이름 미지정
            file_name=str(uploadedFile)
        file_name = self.fileNameCheck(self.user, file_name)

        if uploadedFile != None:
            self.fileSaveForm(user_id=self.user
                        ,file_Title=file_name,file_Root=uploadedFile)
        return 0
    #fileDelete는 무조건 request를 통해 받아야함
    def fileDelete(self, request):
        files = request.POST.get('data')
        files = json.loads(files)
        print(files)
        for i in range(len(files)):
            file_object=File_db.objects.get(user_id=self.user,file_Title=files[i])
            file_object.delete()
            try:
                os.remove('./media/' + str(file_object.file_Root))
            except FileNotFoundError:
                print("파일이 이미 삭제된 상태입니다.")
        result = {
                    'result':'success'
                }
                # Redirect to a success page.
        return result
    #파일 저장 함수
    def fileSave(self, result,file_name):#결과 dataframe, object:파일경로
        #전처리 후 excel파일로 변환 > open()을 통해 이진형식 rb로 읽어야 db에 저장가능
        #---------------같은 이름 파일명 처리-------------
        file_name = self.fileNameCheck(self.user, file_name)
        result.to_csv(file_name, index = False)
        #--------------------------------------------------
        f = open(file_name,'rb')
        file_open=File(f,name=file_name)
        self.fileSaveForm(user_id=self.user
                          ,file_Title=file_name,file_Root=file_open)
        f.close()
        os.remove(file_name)
        return 0
    
    def fileGetter(self, file_name):
        if cacheGetter(self.user, file_name) == True:
                cacheData = cacheGetter(self.user, file_name)
                data = pd.read_json(cacheData)
                summary=DataProcess(data).makeSummary()
        else:
            file_object=File_db.objects.get(user_id=self.user, file_Title=file_name)

            work_dir = './media/' + str(file_object.file_Root)
            if os.path.splitext(work_dir)[1] == ".csv":
                try:
                    data=pd.read_csv(work_dir,encoding="cp949")
                except UnicodeDecodeError:
                    data=pd.read_csv(work_dir,encoding="utf-8")
            else:
                data = pd.read_excel(work_dir, sheet_name= 0)
        return data
    
    def fileLoad(self, file_name):
        cacheData = cacheGetter(self.user, file_name)
        if cacheData != False:
            data = pd.read_json(cacheData)
            summary=DataProcess(data).makeSummary()
            data_json = data.to_json(orient="records",force_ascii=False)
        else:
            file_object=File_db.objects.get(user_id=self.user, file_Title=file_name)

            work_dir = './media/' + str(file_object.file_Root)
            if os.path.splitext(work_dir)[1] == ".csv":
                try:
                    data=pd.read_csv(work_dir,encoding="cp949")
                except UnicodeDecodeError:
                    data=pd.read_csv(work_dir,encoding="utf-8")
            else:
                data = pd.read_excel(work_dir, sheet_name= 0)
            summary=DataProcess(data).makeSummary()
            #---------------json생성------------------
            data=data.replace({np.nan: 0}) 
            dateIndex = DataProcess.dateDetecter(data)
            data = DataProcess.columnToString(data, dateIndex)
            data_json=data.to_json(orient="records",force_ascii=False)#데이터프레임을 json배열형식으로변환(형식은 spreadsheet.js에 맞춰)
            cacheSetter(self.user, file_name, data_json)
        
        summary_json = summary.to_json(orient="columns",force_ascii=False)
        context = {
                    'user_name':self.user,
                    'result':'success',
                    'data' : data_json,
                    'summarys' : json.loads(summary_json)
                }
        return context
    
    #다중 파일 로드
    def fileLoadMulti(self, file_names):
        data_json = []
        for file_name in file_names:
            file_object=File_db.objects.get(user_id=self.user, file_Title=file_name)
            work_dir = './media/' + str(file_object.file_Root)
            if os.path.splitext(work_dir)[1] == ".csv":
                try:
                    data=pd.read_csv(work_dir,encoding="cp949")
                except UnicodeDecodeError:
                    data=pd.read_csv(work_dir,encoding="utf-8")
            else:
                data = pd.read_excel(work_dir, sheet_name= 0)
            data_json.append(data.to_json(orient="records",force_ascii=False))#데이터프레임을 json배열형식으로변환(형식은 spreadsheet.js에 맞춰)
        context = {
                    'data' : data_json,
                }
        return context
    #파일 저장 폼
    @staticmethod
    def fileSaveForm(user_id, file_Title, file_Root):
        instance = File_db(
                    user_id=user_id,
                    file_Title=file_Title,
                    file_Root=file_Root,
                )
        instance.save()
    #input : id, file이름 output: 중복되지 않는 파일이름
    @staticmethod
    def fileNameCheck(id, file_name):
        if file_name.split(".")[-1] in ["xlsx","xls","csv"]:
            file_name = "".join(file_name.split(".")[0:-1])
        if File_db.objects.filter(user_id=id, file_Title=file_name+".csv"):
                file_name_copy = copy.copy(file_name)
                unique = 1
                while File_db.objects.filter(user_id=id, file_Title=file_name_copy+".csv"):
                    unique+=1
                    file_name_copy=file_name+"_"+str(unique)
                file_name = file_name_copy
        file_name = file_name + ".csv"
        return file_name

## -------------데이터 변경 클래스-----------------
class DataProcess:
    def __init__(self, data, date = 0):
        self.data = data
        self.date = int(date)

    
    #실수 자료를 소수점 2자리 수로 반올림
    def roundConverter(self):
        data = self.data
        data[data.select_dtypes(exclude=['object']).columns] = data.select_dtypes(exclude=['object']).round(decimals = 2)
        data[data.select_dtypes(include=['object','datetime64[ns]']).columns] = data.select_dtypes(include=['object','datetime64[ns]']).astype(str)

        return 0
    
    #데이터 변경, 결측치,이상치 처리


    #다양한 날짜 형식 처리, 타입 처리 전엔 항상 날짜의 형태의 문자열로 처리, 날짜 열만 따로 호출함.
    def dateConverter(self):
        dateType = self.data.iloc[:, self.date].dtype
        dateColumn = self.data.iloc[:, self.date]
        self.data.rename(columns={self.data.columns[self.date]:'날짜'}, inplace=True)
        print(dateType)
        if dateType == str or dateType == object:
            dateColumn = pd.to_datetime(dateColumn)
        elif dateType in [int, np.int64]:
            dateColumn = pd.to_datetime(dateColumn.astype(str))
        elif dateType == "datetime64[ns]":    
            dateColumn = pd.to_datetime(dateColumn)
        else:
            print("날짜 형식이 아닙니다.")
        self.data.iloc[:, self.date] = dateColumn
        print(self.data.iloc[:, self.date].dtype)
    
    def getDate(self):
        return self.data.iloc[:, self.date]
    
    def makeSummary(self):
        df = self.data
        nullCountData=pd.DataFrame(df.isnull().sum()).T
        nullCountData.index=["Null_count"]
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
    #함수 input과 output은 데이터프레임. json변환은 따로 따로. 초기 변환은 배치처리

    def outLierDropper(self):
        data = self.data
        for i in range(len(data.columns)):
            if data.iloc[:, i].dtype == "int64" or data.iloc[:, i].dtype == "float64":
                data.drop(DataProcess.outLierDetecter(data.iloc[:, i]))
        return data
    
    @staticmethod
    def dataMerger(df1, df2):
        df1 = df1.append(df2)
        return df1
    
    #날짜열의 위치를 탐지. 반드시 날짜 형식이 있어야 함. 없을 시 변화없고 경고문 출력
    @staticmethod
    def dateDetecter(data):
        for i, k in enumerate(data):
            if data[k].dtype == "datetime64[ns]":
                return i
        return -1
    
    @staticmethod
    def intDetecter(data):
        for i, k in enumerate(data):
            if data[k].dtype == "int64":
                return i
        return -1
    
    #컬럼명 변경
    @staticmethod
    def columnToString(df, columnIndex):
        if columnIndex != -1:
            df.iloc[:, columnIndex] = df.iloc[:, columnIndex].astype(str)
        return df
    
    #하나의 series를 받아서 결측치의 인덱스를 알려줌
    @staticmethod
    def outLierDetecter(data):
        min = data.mean()+3*data.std()
        max = data.mean()-3*data.std()
        mask = ((data > min) | (data < max))
        index = np.where(mask)[0]
        print(index)
        return index
    
@staticmethod
class JsonProcess:
    def jsonToDf(json):
        data = pd.DataFrame(json)
        return data

def dataJoiner(df1, df2, left_key, right_key):
    joinedData = pd.merge(df1, df2, left_on=left_key, right_on=right_key, how='left')
    return joinedData

def cacheSetter(user, file_name, data):
    cacheID = File_db.objects.get(user_id=user, file_Title=file_name).id
    cache.set(cacheID, data, timeout=60)

def cacheGetter(user, file_name):
    cacheID = File_db.objects.get(user_id=user, file_Title=file_name).id
    if cache.get(cacheID):
        print("캐싱된 데이터입니다.")
        return cache.get(cacheID)
    else:
        return False