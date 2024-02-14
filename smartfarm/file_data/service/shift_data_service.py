from .get_file_data_service import GetFileDataService
from ...file.utils.utils import search_file_absolute_path
from ...file.service.file_save_service import FileSaveService
from ..exceptions.file_data_exceptions import FileNotCompleteException
from ...models import File, Temp, FileStatus, TempStatus
import pandas as pd
class ShiftDataService():
    def __init__(self, user, file_object, window_size, count, new_file_name, feature):
        self.user = user
        self.file_object = file_object
        self.window_size = window_size
        self.count = count
        self.new_file_name = new_file_name
        self.feature = feature
        
    @classmethod    
    def from_serializer(cls, serializer, user):
        file_object = serializer.get_temp_object_or_original(user, status_id = 4)
        print(file_object)
        return cls(user
                   ,file_object
                   ,serializer.validated_data["windowSize"]
                   ,serializer.validated_data["count"]
                   ,serializer.validated_data["newFileName"]
                   ,serializer.validated_data["feature"])
    
    def execute(self):
        #전처리가 완료된 파일일 경우에만 실행// merge됐거나 전처리가 완료된...
        
        if isinstance(self.file_object, Temp) and TempStatus.objects.filter(temp_id=self.file_object.id, status_id=4).exists() == False:
            raise FileNotCompleteException()
        
        file_absolute_path = search_file_absolute_path(self.file_object.file_root)
        #변할 가능성 있음
        df = GetFileDataService.file_to_df(file_absolute_path)

        df = df[self.feature]

        shifted_dfs = [df]
        original_columns = df.columns
        for i in range(self.count):
            # 데이터프레임을 이동시킴
            df = df.shift(periods=self.window_size, axis=0)
            df.columns = [f'{col}_{i+1}' for col in original_columns]
            # 이동된 데이터프레임을 리스트에 추가
            shifted_dfs.append(df)

            # 리스트에 저장된 데이터프레임을 concat하여 합침
        merged_df = pd.concat(shifted_dfs, axis=1)
        #df = self.rolling_data(df, self.window_size, self.date_column)
        FileSaveService(self.user, self.new_file_name, merged_df, statuses=5).execute()
    
    @staticmethod
    def rolling_data(df, window_size, date_column):
        return df.rolling(on=[date_column], window=window_size)