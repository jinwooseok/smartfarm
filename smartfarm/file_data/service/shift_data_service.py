from .get_file_data_service import GetFileDataService
from ...file.utils.utils import search_file_absolute_path
from ...file.service.temp_save_service import TempSaveService
from ..exceptions.file_data_exceptions import FileNotCompleteException

class ShiftDataService():
    def __init__(self, user, file_object, window_size):
        self.user = user
        self.file_object = file_object
        self.window_size = window_size
        self.date_column = 0
        
    @classmethod    
    def from_serializer(cls, user, serializer):
        return cls(user, serializer.file_object, serializer.windowSize)
    
    def execute(self):
        #전처리가 완료된 파일일 경우에만 실행
        if self.file_object.statuses != 2:
            raise FileNotCompleteException()
        
        file_absolute_path = search_file_absolute_path(self.file_root)
        #변할 가능성 있음
        df = GetFileDataService.file_to_df(file_absolute_path)
        df = self.rolling_data(df, self.window_size, self.date_column)
        TempSaveService(self.user, self.file_title, df, statuses=5).execute()
    
    @staticmethod
    def rolling_data(df, window_size, date_column):
        return df.rolling(on=df.columns[date_column], window=window_size)