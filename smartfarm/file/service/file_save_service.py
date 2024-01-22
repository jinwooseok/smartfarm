from ...models import File, user_file_path
import pandas as pd
from django.core import files
import copy
import os
from django.db import transaction

from ..utils.utils import *
from ..exceptions.file_exception import *

from ...feature.serializers import FeatureSerializer
from ...feature.service.feature_service import FeatureService
from common.validate_exception import ValidationException
class FileSaveService():
    
    def __init__(self, serializer, user):
        self.user = user
        self.file_title = serializer.validated_data['fileName']
        self.file_data = serializer.validated_data['fileData']

    @transaction.atomic
    def execute(self):
        #파일명 중복 체크
        self.file_title = self.convert_file_name(self.user, self.file_title)
        #데이터 배열을 csv파일로 만들기
        self.json_to_csv(self.file_title, self.file_data)

        FileSaveService.save_file(self.user, self.file_title)
        file = File.objects.get(user_id=self.user, file_title=self.file_title)
        print(file.id)
        feature_info_list = FeatureService.extract_feature(file.id, pd.DataFrame(self.file_data))
        print(feature_info_list)
        #변수 정보 저장
        feature_serializer = FeatureSerializer(data=feature_info_list, many=True)
        if feature_serializer.is_valid():
            feature_serializer.save()
        else:
            raise ValidationException(feature_serializer)
        #파일 저장
    
        


    
    @staticmethod
    def json_to_csv(file_title, file_data):
        data = pd.DataFrame(file_data)
        data.to_csv(file_title, index = False)

    @staticmethod
    def save_file(user, file_title):
        f = open(file_title,'rb')
        file_open=files.File(f, name=file_title)
        instance = FileSaveService.save_file_form(user, file_title, file_open)
        instance.save()
        f.close()
        os.remove(file_title)
    
    @staticmethod
    def save_file_form(user, file_title, file_root):
        instance = File(
                    user_id=user,
                    file_title=file_title,
                    file_root=file_root,
                )
        return instance

    #input : id, file이름 output: 중복되지 않는 파일이름
    @staticmethod
    def convert_file_name(user, file_title):
        no_suffix_file_title = FileSaveService.remove_file_suffix(file_title)
        processed_file_title = FileSaveService.process_duplicated_file_name(user, no_suffix_file_title)
        return processed_file_title + ".csv"
    
    @staticmethod
    def remove_file_suffix(file_title):
        if file_title.split(".")[-1] in ["xlsx","xls","csv"]:
            file_title = "".join(file_title.split(".")[0:-1])
        return file_title
    
    @staticmethod
    def process_duplicated_file_name(user, file_title):
        file_title_copy = copy.copy(file_title)
        unique=1
        while File.objects.filter(user_id=user, file_title=file_title_copy+".csv").exists():
            file_title_copy=file_title+"_"+str(unique)
            unique+=1
        return file_title_copy
