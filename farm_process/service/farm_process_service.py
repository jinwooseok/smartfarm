"""
파일 데이터를 가공하는 서비스
"""
from file_data.service.get_file_data_service import GetFileDataService
from file.utils.utils import search_file_absolute_path
from file.service.temp_save_service import FileSaveService
from file.service.temp_delete_service import TempDeleteService
from farm_process.utils.process import ETLProcessFactory
from file_data.service.get_temp_data_service import GetTempDataService
from common.exceptions import *

class FarmProcessService():
    """
    설명
    - 모델 생성 서비스 클래스. 모든 모델 생성 서비스를 분기하는 클래스이다.
    
    메서드
    - __init__(self, serializer, user) : 초기화 메서드
    - execute(self) : 서비스 실행 메서드
    """

    def __init__(self, serializer, user):
        """
        설명
            초기화 메서드
        매개변수
            serializer : 시리얼라이저
            user : 사용자 객체
        """
        self.new_file_name = serializer.validated_data['newFileName']
        self.file_type = serializer.validated_data['fileType']
        self.interval = serializer.validated_data['interval']
        self.var = serializer.validated_data['var']
        self.file_object = serializer.get_file_object(user)
        self.file_root = self.file_object.file_root
        self.user = user

    def execute(self):
        """
        설명
            서비스 실행 메서드    
        
        서비스 로직
        1. 파일 데이터를 불러온다.
        2. 프로세스를 선정한다.
        3. 프로세스를 실행한다.
        4. 결과를 저장한다.
        5. 임시파일을 삭제한다.
        """
        #날짜 컬럼이 없을 경우 예외 발생
        if self.file_object.date_column is None:
            raise DateColumnException()
        #임시파일 불러오기
        instance = GetTempDataService.get_temp_file(self.file_object.id, status_id=1)
        #파일 절대 경로를 통해 불러오기
        file_absolute_path = search_file_absolute_path(instance.file_root)
        #파일을 데이터프레임으로 변환
        df = GetFileDataService.file_to_df(file_absolute_path)
        #프로세스 선정
        process_factory = ETLProcessFactory(df, self.file_type, self.interval, var = self.var)
        #정적 메서드 핸들러
        result = process_factory.handler()
        #저장
        FileSaveService(self.user, self.new_file_name, result, '날짜', 1,statuses=2).execute()
        #임시파일 삭제
        TempDeleteService(self.user, instance).execute()
