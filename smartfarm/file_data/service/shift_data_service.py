from .get_file_data_service import GetFileDataService
from ...file.utils.utils import search_file_absolute_path
from ...file.service.file_save_service import FileSaveService
from ...file.service.temp_save_service import TempSaveService
import pandas as pd
from ..utils.process import DataProcess
from ..exceptions.file_data_exceptions import YValueDuplicateException, RequiredValueException
class ShiftDataService():
    def __init__(self, user, file_object, count, xValue, yValue):
        self.user = user
        self.file_object = file_object
        self.window_size = 1
        self.count = count
        self.xValue = xValue
        self.yValue = yValue
        
    @classmethod    
    def from_serializer(cls, serializer, user):
        file_object = serializer.get_file_object(user)
        return cls(user
                   ,file_object
                   ,serializer.validated_data["count"]
                   ,serializer.validated_data["xValue"]
                   ,serializer.validated_data["yValue"])
    
    def execute(self):
        if self.yValue in self.xValue:
            raise YValueDuplicateException(self.yValue)
        if None in [self.xValue, self.yValue]:
            raise RequiredValueException()
        file_absolute_path = search_file_absolute_path(self.file_object.file_root)
        #변할 가능성 있음
        df = GetFileDataService.file_to_df(file_absolute_path)
        x_df = df[self.xValue]
        y_df = df[self.yValue]
        shifted_dfs = [x_df]
        original_columns = x_df.columns
        for i in range(self.count):
            # 데이터프레임을 이동시킴
            x_df = x_df.shift(periods=self.window_size, axis=0)
            x_df.columns = [f'{col}_{i+1}' for col in original_columns]
            # 이동된 데이터프레임을 리스트에 추가
            shifted_dfs.append(x_df)

            # 리스트에 저장된 데이터프레임을 concat하여 합침
        shifted_dfs.append(y_df)
        merged_df = pd.concat(shifted_dfs, axis=1)

        return DataProcess.df_to_json_object(merged_df)