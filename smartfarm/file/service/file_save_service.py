from ...models import File, FileStatus
import pandas as pd
from django.core import files
import copy
import os
from django.db import transaction
from ..utils.utils import *
from ..exceptions.file_exception import *
from ...farm_process.exceptions.exceptions import StartIndexException
from ..repositorys import *

class FileSaveService():
    
    def __init__(self, user, file_title, file_data, date_column=None, start_index=1, statuses=1):
        self.user = user
        self.file_title:str = file_title
        self.file_data = file_data
        self.statuses:int = statuses
        self.date_column:str = date_column
        self.start_index:int = start_index

    @classmethod
    def from_serializer(cls, serializer, user) -> 'FileSaveService':
        return cls(user
                   ,serializer.validated_data['fileName']
                   ,serializer.validated_data['fileData']
                   ,serializer.validated_data['dateColumn']
                   ,serializer.validated_data['startIndex'])

    @transaction.atomic
    def execute(self) -> None:
        #파일명 중복 체크
        self.file_title = self.convert_file_name(self.user, self.file_title)
        #데이터 배열을 csv파일로 만들기
        if type(self.file_data) is not pd.DataFrame:
            self.file_data = pd.DataFrame(self.file_data)
        
        if self.start_index < 1 or self.start_index > len(self.file_data):
            raise StartIndexException()
        elif self.start_index > 1:
            self.file_data = self.file_data[self.start_index-1:]
            self.start_index = 1
        
        if self.date_column is None:
            self.date_column = self.file_data.columns[0]
        
        if self.date_column != self.file_data.columns[0]:
            date_series = self.file_data.pop(self.date_column)
            self.file_data.insert(0, self.date_column, date_series)
        self.data_to_csv(self.file_title, self.file_data)
        self.save_file()
    
    def save_file(self):
        try:
            f = open(self.file_title,'rb')
            file_open=files.File(f, name=self.file_title)
            instance = self.file_form(self.user
                                      ,self.file_title
                                      ,file_open
                                      ,self.date_column
                                      ,self.start_index)
            instance.save()
        except:
            raise FileSaveException()
        
        FileStatus.objects.create(status_id=self.statuses, file_id=instance.id)
        f.close()
        os.remove(self.file_title)
    
    @staticmethod
    def file_form(user, file_title, file_root, date_column, start_index):
        return File(
                    user_id=user,
                    file_title=file_title,
                    file_root=file_root,
                    date_column=date_column,
                    start_index=start_index
                )
    
    @staticmethod
    def data_to_csv(file_title, file_data):
        if type(file_data) is pd.DataFrame:
            FileSaveService.df_to_csv(file_title, file_data)
        elif type(file_data) is list:
            FileSaveService.json_to_csv(file_title, file_data)
        else:
            raise DataToCsvException()

    @staticmethod
    def df_to_csv(file_title, file_data:list)->None:
        file_data.to_csv(file_title, index = False)
    
    @staticmethod
    def json_to_csv(file_title, file_data:pd.DataFrame)->None:
        data = pd.DataFrame(file_data)
        data.to_csv(file_title, index = False)

    #input : id, file이름 output: 중복되지 않는 파일이름
    @staticmethod
    def convert_file_name(user, file_title, suffix=".csv"):
        no_suffix_file_title = FileSaveService.remove_file_suffix(file_title)
        processed_file_title = FileSaveService.process_duplicated_file_name(user, no_suffix_file_title, suffix)
        return processed_file_title
    
    @staticmethod
    def remove_file_suffix(file_title):
        if file_title.split(".")[-1] in ["xlsx","xls","csv"]:
            file_title = "".join(file_title.split(".")[0:-1])
        return file_title
    
    @staticmethod
    def process_duplicated_file_name(user, file_title, suffix):
        file_title_copy = copy.copy(file_title)
        unique=1
        while exist_file_by_user_file_title(user, file_title_copy + suffix):
            file_title_copy=file_title+"_"+str(unique)
            unique+=1
        return file_title_copy + suffix
