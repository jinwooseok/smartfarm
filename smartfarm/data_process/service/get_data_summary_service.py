from ...file_process.utils.utils import *
import pandas as pd
from ..utils.process import DataProcess
import os
import json
from .get_file_data_service import GetFileDataService
from ..utils.process import DataProcess
class GetDataSummaryService():
    def __init__(self, serializer, user):
        self.file_name = serializer.data['fileName']
        self.file_root = serializer.get_file_root(user)
        self.file_object = serializer.get_file_object(user)
    
    def execute(self):
        file_absolute_path = search_file_absolute_path(self.file_root)
        dataFrame = GetFileDataService.file_to_df(file_absolute_path)
        
        data = DataProcess.round_converter(dataFrame)
        data = DataProcess.non_to_blank(data) 
        return DataProcess.to_summary(data)
        # return json.loads(DataProcess.df_to_json_string(data))