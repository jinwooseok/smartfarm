"""
모델을 저장하는 서비스를 제공하는 파일
"""
import datetime
from django.db import transaction
from file.service.file_save_service import FileSaveService
from analytics.models import LearnedModel
from file.models import File

class SaveModelService(FileSaveService):
    """
    설명
    - 생성한 모델을 저장하는 클래스. FileSaveService를 상속받아 구현
    
    메서드
    - __init__ : 생성자
    - execute : 모델 저장 실행
    - model_form : 모델 정보 저장 형식 Entity
    - save_model : DB와 파일시스템에 모델 저장을 수행
    - process_duplicated_file_name : model 파일명 중복 처리 
    """
    def __init__(self, file_object, model, model_name, model_meta) -> "SaveModelService":
        """
        매개변수
        - file_object : File 객체
        - model : 저장할 모델
        - model_name : 모델명
        - model_meta : 모델 메타 정보
        - user : 사용자 객체
        """
        super().__init__(file_object.user, model_name, model)
        self.model = model
        self.file_object:File = file_object
        self.model_name:str = model_name
        self.model_meta:dict = model_meta
        self.user = file_object.user

    @transaction.atomic
    def execute(self):
        """
        설명
        - 모델을 저장하는 메서드
        - 모델을 저장하고 모델 정보를 저장한다.
        
        반환값
        - model_object : 저장된 모델 객체
        """
        # 1. 파일명(모델 피클 파일 + 메타 데이터 파일) 중복체크
        model_file_name = self.convert_file_name(self.user, self.model_name, ".pkl")
        model_meta_file_name = self.convert_file_name(self.user, self.model_name+"_meta", ".json")   

        # 2. savev_model 함수를 통해 모델 저장
        model_object = self.save_model(self.model,
                                       self.model_meta,
                                       model_file_name,
                                       model_meta_file_name)
        return model_object

    def model_form(self, user, model_name, model_meta_name):
        """
        설명
        - 모델 정보 저장 형식 Entity를 반환하는 메서드
        
        매개변수
        - user : 사용자 객체
        - model_name : 모델명
        - model_meta_name : 모델 메타 정보명
        
        반환값
        - LearnedModel Entity
        """
        return LearnedModel(user=user
                            ,original_file_name=self.file_object.file_title
                            ,model_name=model_name
                            ,model_meta_name=model_meta_name)     

    def save_model(self, model, model_meta, model_file_name, model_info_file_name):
        """
        설명
        - model_form으로 객체를 불러온 후 save를 통해 모델 저장을 수행
        - DB에 저장한 후 utils/signals.py 파일을 통해 파일 시스템에 저장
        
        매개변수
        - model : 저장할 모델
        - model_meta : 모델 메타 정보
        - model_file_name : 모델 파일명
        - model_info_file_name : 모델 정보 파일명
        
        반환값
        - model_form : 저장된 모델
        """
        model_form = self.model_form(self.user, model_file_name, model_info_file_name)
        model_form.save(model, model_meta)
        return model_form

    def process_duplicated_file_name(self, user, file_title, suffix):
        """
        설명
        - model 파일명 중복 처리
        
        매개변수
        - user : 사용자 객체
        - file_title : 파일명
        - suffix : 파일 확장자
        
        반환값
        - 중복되지 않는 파일명
        """
        return file_title+"_" + user + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + suffix
