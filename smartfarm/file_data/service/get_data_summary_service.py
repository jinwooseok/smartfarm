from ...file.utils.utils import *
from ..utils.process import DataProcess
from .get_file_data_service import GetFileDataService
import pandas as pd

class GetDataSummaryService():
    def __init__(self, serializer, user):
        self.file_name = serializer.data['fileName']
        self.file_root = serializer.get_file_root(user)
        self.file_object = serializer.get_file_object(user)
    
    def execute(self):
        file_absolute_path = search_file_absolute_path(self.file_root)
        df = GetFileDataService.file_to_df(file_absolute_path)
        
        return GetDataSummaryService.to_summary(df)
        # return json.loads(DataProcess.df_to_json_string(data))
    
    @staticmethod
    def to_summary(data):
        drop_list = []
        for column in data.columns:
            if DataProcess.to_numeric_or_none(data[column]) is None:
                drop_list.append(column)
        
        data = DataProcess.drop_columns(data, drop_list)
            
        null_count=pd.DataFrame(data.isnull().sum()).T
        null_count.index=["Null_count"]
        statistic_info = data.describe().iloc[[4,5,6,1,3,7],:]
        
        statistic_info.index = ["Q1","Q2","Q3","mean","min","max"]

        # column_name = pd.Series({"name":list(data.columns)})
        columns_df = pd.DataFrame([data.columns], index=['name'], columns=data.columns)

        summary = pd.concat([columns_df,null_count,statistic_info], ignore_index=False)
        summary = DataProcess.nan_to_string(summary, "-")
        summary = DataProcess.round_converter(summary)

        return DataProcess.df_to_json_object(summary.T, orient="records")