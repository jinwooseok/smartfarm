from .file_save_service import FileSaveService
from ...models import Temp, TempStatus, File
import pandas as pd
from django.core import files
import copy
import os
from django.db import transaction

class TempSaveService(FileSaveService):
    
    def __init__(self, user, file_title, new_file_title, file_data, statuses=None):
        self.user = user
        self.file_title = file_title
        self.new_file_title = new_file_title
        self.file_data = file_data
        self.statuses = statuses

    @transaction.atomic
    def execute(self):
        #파일명 중복 체크
        self.file_title = self.convert_file_name(self.user, self.file_title)
        #데이터 배열을 csv파일로 만들기
        self.data_to_csv(self.file_title, self.file_data)
        
        file = File.objects.get(user_id=self.user, file_title=self.file_title)
        
        TempSaveService.save_file(file.id, self.new_file_title, self.statuses)


    @staticmethod
    def save_file(file_id, file_title, statuses):
        f = open(file_title,'rb')
        file_open=files.File(f, name=file_title)
        instance = TempSaveService.save_file_form(file_id, file_title, file_open)
        instance.save()
        TempStatus.objects.create(status_id=statuses, file_id=instance.id)
        f.close()
        os.remove(file_title)
    
    @staticmethod
    def save_file_form(file_id, file_title, file_root, file_type=None):
        instance = Temp(
                    file_id = file_id,
                    file_type = file_type,
                    file_title=file_title,
                    file_root=file_root
                )
        return instance

    #input : id, file이름 output: 중복되지 않는 파일이름
    @staticmethod
    def convert_file_name(user, file_title):
        no_suffix_file_title = FileSaveService.remove_file_suffix(file_title)
        processed_file_title = TempSaveService.process_duplicated_file_name(user, no_suffix_file_title)
        return processed_file_title + ".csv"

    @staticmethod
    def process_duplicated_file_name(file_id, file_title):
        file_title_copy = copy.copy(file_title)
        unique=1
        while Temp.objects.filter(file_id=file_id, file_title=file_title_copy+".csv").exists():
            file_title_copy=file_title+"_"+str(unique)
            unique+=1
        return file_title_copy
