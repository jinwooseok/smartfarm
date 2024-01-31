from .file_save_service import FileSaveService
from .file_delete_service import FileDeleteService
from ...models import Temp, TempStatus, File
from django.core import files
import copy
import os
from django.db import transaction

class TempSaveService(FileSaveService):
    
    def __init__(self, user, file_title, file_data, statuses=None):
        self.user = user
        self.file_title = file_title
        self.file_data = file_data
        self.statuses = statuses

    @transaction.atomic
    def execute(self):
        #파일명 중복 체크
        file_title = self.convert_file_name(self.user, self.file_title)
        #데이터 배열을 csv파일로 만들기
        self.data_to_csv(file_title, self.file_data)
        
        file = File.objects.get(user_id=self.user, file_title=file_title)
        
        TempSaveService.save_file(file, file_title, self.statuses)


    @staticmethod
    def save_file(file, file_title, statuses):
        f = open(file_title,'rb')
        file_open=files.File(f, name=file_title)
        try:
            #있는데 root만 달라진거면 새 root로 저장하고 기존 root 삭제
            print(file)
            temp_instance = Temp.objects.get(file=file)
            if temp_instance.file_root != file_open:
                temp_instance.delete()
                Temp.objects.create(file=file, file_title=file_title, file_root=file_open)
        #없으면 새로 저장
        except Temp.DoesNotExist:
            Temp.objects.create(file=file, file_title=file_title, file_root=file_open)
        f.close()
        os.remove(file_title)

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
