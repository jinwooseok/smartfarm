"""
file save service를 상속받아 temp file save service를 구현. 임시 저장 서비스
"""
from file.service.file_save_service import FileSaveService
from file.repositorys import *
from file.models import Temp, TempStatus
from django.core import files
import copy
import os
from django.db import transaction

class TempSaveService(FileSaveService):
    """
    임시 저장 서비스를 제공하는 클래스
    
    Attributes:
    ----------
    user : int
        사용자 id
    file_title : str
        파일 이름
    file_data : pd.DataFrame
        파일 데이터
    new_file_title : str
        새 파일 이름
    file_type : str
        파일 타입
    statuses : list
        파일 상태
    
    Methods:
    -------
    execute : str
        임시 저장 실행
    save_file : None
        파일 저장
    process_duplicated_file_name : str
        중복되지 않는 파일 이름 생성
    """
    def __init__(self, user, file_title, file_data, new_file_title=None, file_type=None, statuses=None):
        self.user = user
        self.file_title = file_title
        self.file_data = file_data
        self.new_file_title = new_file_title
        self.file_type = file_type
        self.statuses = statuses

    @transaction.atomic
    def execute(self):
        """
        기존 저장된 파일을 불러와 새로운 임시 파일로 저장
        """
        file = get_file_by_user_file_title(self.user, self.file_title)
        #파일명 중복 체크
        if self.new_file_title:
            self.file_title = self.new_file_title
        file_title = self.convert_file_name(self.user, self.file_title)
        #데이터 배열을 csv파일로 만들기
        self.data_to_csv(file_title, self.file_data)
        TempSaveService.save_file(file, file_title, self.file_type, self.statuses)
        return file_title

    @staticmethod
    def save_file(file, file_title, file_type, statuses):
        """
        파일 저장
        """
        f = open(file_title,'rb')
        file_open=files.File(f, name=file_title)
        try:
            #있는데 root만 달라진거면 새 root로 저장하고 기존 root 삭제
            temp_instance = Temp.objects.get(file=file)
            if temp_instance.file_root != file_open:
                temp_instance.delete()
                instance = Temp.objects.create(file=file, file_title=file_title, file_type = file_type, file_root=file_open)
        #없으면 새로 저장
        except Temp.DoesNotExist:
            instance = Temp.objects.create(file=file, file_title=file_title, file_type = file_type, file_root=file_open)
        for status in statuses:
            TempStatus.objects.create(temp_id=instance.id, status_id=status)
        f.close()
        os.remove(file_title)

    def process_duplicated_file_name(self, file_id, file_title, suffix):
        """
        중복되지 않는 파일 이름 생성-오버라이딩(temp모델과 file모델을 구분하기 위해 수정)
        """
        file_title_copy = copy.copy(file_title)
        unique=1
        while Temp.objects.filter(file_id=file_id, file_title=file_title_copy+suffix).exists():
            file_title_copy=file_title+"_"+str(unique)
            unique+=1
        return file_title_copy + suffix
