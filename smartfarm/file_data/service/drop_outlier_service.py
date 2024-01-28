from .get_file_data_service import GetFileDataService
from ...file.utils.utils import search_file_absolute_path
from ..utils.process import DataProcess
from ...file.service.file_save_service import FileSaveService
class ProcessOutlierService():
    def __init__(self, file_name, file_root, file_object, new_file_name, user):
        self.user = user
        self.file_name = file_name
        self.file_root = file_root
        self.file_object = file_object
        self.new_file_name = new_file_name
    
    @classmethod
    def from_serializer(cls, serializer, user) -> 'ProcessOutlierService':
        return cls(serializer.data['fileName']
                   ,serializer.get_file_root(user)
                   ,serializer.get_file_object(user)
                   ,serializer.data['newFileName']
                   ,user)
    

    def execute(self):
            file_absolute_path = search_file_absolute_path(self.file_root)
            df = GetFileDataService.file_to_df(file_absolute_path)
            df = ProcessOutlierService.outlier_dropper(df)
            FileSaveService(self.user, self.new_file_name, df).execute()
            

    @staticmethod
    def outlier_dropper(df):
        drop_index = []
        for column in df.columns:
            numeric_column = DataProcess.to_numeric_or_none(df[column])
            if numeric_column is not None:
                drop_index = drop_index+DataProcess.outlier_detector(df[column])

        return DataProcess.drop_rows(df, list(set(drop_index)))