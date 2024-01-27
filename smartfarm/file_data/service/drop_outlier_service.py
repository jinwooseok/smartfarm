from .get_file_data_service import GetFileDataService
from ...file.utils.utils import search_file_absolute_path
from ..utils.process import DataProcess

class ProcessOutlierService():
    def __init__(self, serializer, user):
        self.file_name = serializer.data['fileName']
        self.file_root = serializer.get_file_root(user)
        self.file_object = serializer.get_file_object(user)

    def execute(self):
            file_absolute_path = search_file_absolute_path(self.file_root)
            df = GetFileDataService.file_to_df(file_absolute_path)
            return df

    @staticmethod
    def outlier_dropper(df):
        drop_index = []
        for column in df.columns:
            numeric_column = DataProcess.to_numeric_or_none(df[column])
            if numeric_column is not None:
                drop_index = drop_index+DataProcess.outlier_detector(df[column])

        return DataProcess.drop_rows(df, list(set(drop_index)))