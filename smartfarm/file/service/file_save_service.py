from ...models import File, FileStatus
import pandas as pd
from django.core import files
import copy
import os
from django.db import transaction

from ..utils.utils import *
from ..exceptions.file_exception import *

from ...feature.serializers import FileFeatureSerializer
from ...feature.service.feature_service import FeatureService
from common.validators import serializer_validator
from ..repositorys import *

class FileSaveService():
    
    def __init__(self, user, file_title, file_data, statuses=1):
        self.user = user
        self.file_title = file_title
        self.file_data = file_data
        self.statuses = statuses

    @classmethod
    def from_serializer(cls, serializer, user) -> 'FileSaveService':
        return cls(user, serializer.validated_data['fileName'], serializer.validated_data['fileData'])

    @transaction.atomic
    def execute(self):
        #파일명 중복 체크
        self.file_title = self.convert_file_name(self.user, self.file_title)
        #데이터 배열을 csv파일로 만들기
        self.data_to_csv(self.file_title, self.file_data)

        FileSaveService.save_file(self.user, self.file_title, self.statuses)
        
        file = get_file_by_user_file_title(user_id=self.user, file_title=self.file_title)

        feature_info_list = FeatureService.extract_feature(file.id, pd.DataFrame(self.file_data))
        #변수 정보 저장
        feature_serializer = FileFeatureSerializer(data=feature_info_list, many=True)
        feature_serializer = serializer_validator(feature_serializer)
        feature_serializer.save()
        
    @staticmethod
    def data_to_csv(file_title, file_data):
        if type(file_data) is pd.DataFrame:
            return FileSaveService.df_to_csv(file_title, file_data)
        elif type(file_data) is list:
            return FileSaveService.json_to_csv(file_title, file_data)
        else:
            raise DataToCsvException()

    @staticmethod
    def df_to_csv(file_title, file_data):
        file_data.to_csv(file_title, index = False)
    
    @staticmethod
    def json_to_csv(file_title, file_data):
        data = pd.DataFrame(file_data)
        data.to_csv(file_title, index = False)

    @staticmethod
    def save_file(user, file_title, statuses):
        try:
            f = open(file_title,'rb')
            file_open=files.File(f, name=file_title)
            instance = FileSaveService.file_form(user, file_title, file_open)
            instance.save()
        except:
            raise FileSaveException()
        
        FileStatus.objects.create(status_id=statuses, file_id=instance.id)
        f.close()
        os.remove(file_title)
    
    @staticmethod
    def file_form(user, file_title, file_root):
        instance = File(
                    user_id=user,
                    file_title=file_title,
                    file_root=file_root
                )
        return instance

    #input : id, file이름 output: 중복되지 않는 파일이름
    @staticmethod
    def convert_file_name(user, file_title):
        no_suffix_file_title = FileSaveService.remove_file_suffix(file_title)
        processed_file_title = FileSaveService.process_duplicated_file_name(user, no_suffix_file_title)
        return processed_file_title
    
    @staticmethod
    def remove_file_suffix(file_title):
        if file_title.split(".")[-1] in ["xlsx","xls","csv"]:
            file_title = "".join(file_title.split(".")[0:-1])
        return file_title
    
    @staticmethod
    def process_duplicated_file_name(user, file_title):
        file_title_copy = copy.copy(file_title)
        unique=1
        while exist_file_by_user_file_title(user, file_title_copy + ".csv"):
            file_title_copy=file_title+"_"+str(unique)
            unique+=1
        return file_title_copy + ".csv"
