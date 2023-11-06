from ..decorators import logging_time
import pandas as pd
import numpy as np
import os
import copy
import json
from django.http import HttpResponse
#---------------모델 import---------------------
from ..models import File
from django.core import files

## -------------파일 처리 클래스-----------------
#--------------캐시 처리 라이브러리-------------
from django.core.cache import cache
#---------------repository import----------------
from ..repositorys import *
from config.settings import MEDIA_ROOT
from .DataProcess import DataProcess

class FileSystem:
    #백엔드에서 파일처리
    def __init__(self, user, file_title = None, multi_part_file = None, data = None):
        self.user = user
        self.file_title = file_title
        self.multi_part_file = multi_part_file
        self.data = data

    def getFileObjectList(self):
        file_list=findFileObjectListByUserId(self.user)
        return file_list
    
    #파일 업로드 함수 - 처음 파일을 등록하는 함수
    def fileUpload(self):
        if self.multi_part_file is None:
            return HttpResponse("<script>alert('파일이 존재하지 않습니다.');</script>")
        if self.file_title is None:
            self.file_title = self.multi_part_file.name
        
        
        self.file_title = self.fileNameCheck()
        print(self.file_title)
        self.fileSaveForm(self.user,self.file_title,self.multi_part_file)
        
        if self.multi_part_file.name.split(".")[-1] in ["xlsx","xls"]:
            file_object = findFileObjectByUserIdFileTitle(self.user, self.file_title)
            self.file_title = file_object.file_title
            self.data = self.fileLoad()
            self.fileDelete()
            self.fileSave()
        

        
    #fileDelete는 무조건 request를 통해 받아야함
    def fileDelete(self):
        file_object = findFileObjectByUserIdFileTitle(self.user, self.file_title)
        try:
            work_dir = os.path.join(MEDIA_ROOT, str(file_object.file_root))
            os.remove(work_dir)
            file_object.delete()
        except FileNotFoundError:
            return HttpResponse("<script>alert('파일 삭제를 실패했습니다.');</script>")
            # Redirect to a success page.

    #파일 저장 함수
    def fileSave(self):#결과 dataframe, object:파일경로
        #전처리 후 excel파일로 변환 > open()을 통해 이진형식 rb로 읽어야 db에 저장가능
        #---------------같은 이름 파일명 처리-------------
        file_title = self.fileNameCheck()
        if self.data is not None:
            data = pd.read_json(self.data)
            data.to_csv(file_title, index = False)
        #--------------------------------------------------
        f = open(file_title,'rb')

        file_open=files.File(f,name=file_title)
        
        self.fileSaveForm(self.user,file_title,file_open)
        
        f.close()
        os.remove(file_title)
    
    #유저명과 파일명을 통해 데이터를 가져옴
    def fileLoad(self):
        # cache_data = self.cacheGetter()
        # if cache_data is not None:
        #     print("캐싱된 데이터입니다.")
        #     return cache_data         
    
        file_object=findFileObjectByUserIdFileTitle(self.user, self.file_title)
        work_dir = './media/' + str(file_object.file_root)
        print(work_dir)
        if os.path.splitext(work_dir)[1] == ".csv":
            try:
                data=pd.read_csv(work_dir,encoding="cp949")
            except UnicodeDecodeError:
                data=pd.read_csv(work_dir,encoding="utf-8")
        else:
            try:
                data = pd.read_excel(work_dir, sheet_name= 0, engine='xlrd')
            except:
                data = pd.read_excel(work_dir, sheet_name= 0, engine='openpyxl')
        #---------------json생성------------------
        data = data.replace({np.nan: 0}) 
        data = DataProcess.roundConverter(data)
        data_json=data.to_json(orient="records",force_ascii=False)#데이터프레임을 json배열형식으로변환(형식은 spreadsheet.js에 맞춰)
        self.cacheSetter(data_json)
        return data_json
    
    def cacheSetter(self,data):
        cache_object = findFileObjectByUserIdFileTitle(self.user, self.file_title)
        cache_id = cache_object.file_id
        cache.set(cache_id, data, timeout=60)

    def cacheGetter(self):
        cache_object = findFileObjectByUserIdFileTitle(self.user, self.file_title)
        cache_id = cache_object.file_id
        if cache.get(cache_id) is None:
            return None    
        return cache.get(cache_id)
    #파일 저장 폼
    def fileSaveForm(self, user,file_title,file_root):
        instance = File(
                    user_id=user,
                    file_title=file_title,
                    file_root=file_root,
                )
        instance.save()

    #input : id, file이름 output: 중복되지 않는 파일이름
    def fileNameCheck(self):
        file_title = self.file_title
        if file_title.split(".")[-1] in ["xlsx","xls","csv"]:
            file_title = "".join(file_title.split(".")[0:-1])
        print(file_title)
        if findFileObjectListByUserIdFileTitle(user_id=self.user, file_title=file_title+".csv"):
            file_title_copy = copy.copy(file_title)
            unique = 1
            while findFileObjectListByUserIdFileTitle(user_id=self.user, file_title=file_title_copy+".csv"):
                unique+=1
                file_title_copy=file_title+"_"+str(unique)
            file_title = file_title_copy

        file_title = file_title + ".csv"
        return file_title
    
    