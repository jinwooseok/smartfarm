from ...file.utils.utils import *
from ..utils.process import DataProcess
from .get_file_data_service import GetFileDataService
import pandas as pd

class GetDataSummaryService():
    def __init__(self, serializer, user):
        self.file_name = serializer.data['fileName']
        self.file_object = serializer.get_file_object(user)
        self.file_root = self.file_object.file_root    
    def execute(self):
        file_absolute_path = search_file_absolute_path(self.file_root)
        df = GetFileDataService.file_to_df(file_absolute_path)
        
        return GetDataSummaryService.to_summary(df)
        # return json.loads(DataProcess.df_to_json_string(data))
    
    @staticmethod
    def to_summary(data):
        summary_dict = {}
        for column in data.columns:
            numeric_column = DataProcess.to_numeric_or_none(data[column])
            if numeric_column is not None:
                summary_dict[column] = numeric_column
            
        data = pd.DataFrame(summary_dict)
            
        null_count=pd.DataFrame(data.isnull().sum()).T
        null_count.index=["Null_count"]
        statistic_info = data.describe().iloc[[4,5,6,1,3,7],:]
        
        statistic_info.index = ["Q1","Q2","Q3","mean","min","max"]
        
        statistic_info = DataProcess.round_converter(statistic_info)
        # column_name = pd.Series({"name":list(data.columns)})
        columns_df = pd.DataFrame([data.columns], index=['name'], columns=data.columns)

        summary = pd.concat([columns_df,null_count,statistic_info], ignore_index=False)

        summary = DataProcess.nan_to_string(summary, "-")

        return DataProcess.df_to_json_object(summary.T, orient="records")