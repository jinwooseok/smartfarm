from ...file.service.file_save_service import FileSaveService
from django.db import transaction
from ...models import LearnedModel, ModelFeature, File
import copy
import json
import datetime
class SaveModelService(FileSaveService):
    def __init__(self, file_object, model, model_name, model_meta) -> "SaveModelService":
        self.model = model
        self.file_object : File = file_object
        self.model_name : str = model_name
        self.model_meta : dict = model_meta
        self.user = file_object.user
    @transaction.atomic
    def execute(self):
        #파일명 중복체크
        model_file_name = self.convert_file_name(self.user, self.model_name, ".pkl")
        print(model_file_name)
        model_meta_file_name = self.convert_file_name(self.user, self.model_name+"_meta", ".json")   
        #모델 저장
        model_object = self.save_model(self.model, self.model_meta, model_file_name, model_meta_file_name)
        return model_object
        #모델 정보 저장
        
    def model_form(self, user, model_name, model_meta_name):
        return LearnedModel(user=user
                            ,original_file_name=self.file_object.file_title
                            ,model_name=model_name
                            ,model_meta_name=model_meta_name)     

    def save_model(self, model, model_meta, model_file_name, model_info_file_name):
        model_form = self.model_form(self.user, model_file_name, model_info_file_name)
        model_form.save(model, model_meta)
        return model_form
        
    def process_duplicated_file_name(self, user, file_title, suffix):
        return file_title+"_" + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + suffix