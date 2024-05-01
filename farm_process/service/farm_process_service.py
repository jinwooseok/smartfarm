from file_data.service.get_file_data_service import GetFileDataService
from file.utils.utils import search_file_absolute_path
from file.service.temp_save_service import FileSaveService
from file.service.temp_delete_service import TempDeleteService
from farm_process.utils.process import ETLProcessFactory
from file_data.service.get_temp_data_service import GetTempDataService
from common.exceptions import *

class FarmProcessService():
    def __init__(self, serializer, user):
        self.new_file_name = serializer.validated_data['newFileName']
        self.file_type = serializer.validated_data['fileType']
        self.interval = serializer.validated_data['interval']
        self.var = serializer.validated_data['var']
        self.file_object = serializer.get_file_object(user)
        self.file_root = self.file_object.file_root
        self.user = user
    
    def execute(self):
        if self.file_object.date_column is None:
            raise DateColumnException()  
        instance = GetTempDataService.get_temp_file(self.file_object.id, status_id=1)
        
        file_absolute_path = search_file_absolute_path(instance.file_root)
        df = GetFileDataService.file_to_df(file_absolute_path)

        #프로세스 선정
        process_factory = ETLProcessFactory(df, self.file_type, self.interval, var = self.var)
        #정적 메서드 핸들러
        result = process_factory.handler()
        #저장
        FileSaveService(self.user, self.new_file_name, result, '날짜', 1,statuses=2).execute()
        #임시파일 삭제
        TempDeleteService(self.user, instance).execute()
        
    


