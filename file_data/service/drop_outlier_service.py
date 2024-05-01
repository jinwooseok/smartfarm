from get_file_data_service import GetFileDataService
from file.utils.utils import search_file_absolute_path
from file_data.utils.process import DataProcess
from file.service.temp_save_service import TempSaveService
class ProcessOutlierService():
    def __init__(self, file_name, file_root, file_object, user):
        self.user = user
        self.file_name = file_name
        self.file_root = file_root
        self.file_object = file_object
    
    @classmethod
    def from_serializer(cls, serializer, user) -> 'ProcessOutlierService':
        file_object = serializer.get_file_object(user)
        return cls(serializer.data['fileName']
            ,file_object.file_root
            ,file_object
            ,user)
    

    def execute(self):
        file_absolute_path = search_file_absolute_path(self.file_root)
        df = GetFileDataService.file_to_df(file_absolute_path)
        result, drop_index = ProcessOutlierService.outlier_dropper(df)
        TempSaveService(self.user, self.file_name, result, statuses=[1]).execute()
        return drop_index

    @staticmethod
    def outlier_dropper(df):
        drop_index = set()
        for column in df.columns:
            numeric_column = DataProcess.to_numeric_or_none(df[column])
            if numeric_column is not None:
                drop_index = drop_index.union(DataProcess.outlier_detector(numeric_column))
        return df.drop(drop_index), drop_index
    