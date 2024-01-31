from ...file_data.service.get_file_data_service import GetFileDataService
from ...file.utils.utils import search_file_absolute_path
from ...file.service.temp_save_service import TempSaveService
from ..utils.process import ETLProcessFactory

class FarmProcessService():
    def __init__(self, serializer, user):
        self.new_file_name = serializer.validated_data['newFileName']
        self.file_type = serializer.validated_data['fileType']
        self.start_index = serializer.validated_data['startIndex']
        self.date_column = serializer.validated_data['dateColumn']
        self.interval = serializer.validated_data['interval']
        self.var = serializer.validated_data['var']
        self.file_object = serializer.get_file_object(user)
        self.file_root = self.file_object.file_root
        self.user = user
    
    def execute(self):
        file_absolute_path = search_file_absolute_path(self.file_root)
        df = GetFileDataService.file_to_df(file_absolute_path)
        #데이터프레임 윗부분 자르기
        df = df.iloc[self.start_index-1:]
        #프로세스 선정
        process_factory = ETLProcessFactory(df, self.file_type, self.date_column, self.interval, var = self.var)
        #정적 메서드 핸들러
        result = process_factory.handler()
        #저장
        TempSaveService(self.user, self.file_object.file_name, self.new_file_name, result, statuses=2).execute()
    


