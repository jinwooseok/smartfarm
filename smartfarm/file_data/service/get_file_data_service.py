from ...file.utils.utils import *
import pandas as pd
from ..utils.process import DataProcess
import os
import json

class GetFileDataService():
    def __init__(self, serializer, user):
        self.file_name = serializer.data['fileName']
        self.file_root = serializer.get_file_root(user)
        self.file_object = serializer.get_file_object(user)
    
    def execute(self):
        file_absolute_path = search_file_absolute_path(self.file_root)
        dataFrame = GetFileDataService.file_to_df(file_absolute_path)
        data = DataProcess.round_converter(dataFrame)
        data = DataProcess.nan_to_string(data) 
        print(dataFrame.dtypes)
        return DataProcess.df_to_json_object(data)
    
    @staticmethod
    def file_to_df(file_absolute_path):
        if os.path.splitext(file_absolute_path)[1] == ".csv":
            return GetFileDataService.csv_to_df(file_absolute_path)
        elif os.path.splitext(file_absolute_path)[1] == ".xlsx" or os.path.splitext(file_absolute_path)[1] == ".xls":
            return GetFileDataService.excel_to_df(file_absolute_path)

    @staticmethod
    def csv_to_df(file_absolute_path):
        try:
            return pd.read_csv(file_absolute_path,encoding="cp949")
        except UnicodeDecodeError:
            return pd.read_csv(file_absolute_path,encoding="utf-8")
        
    @staticmethod
    def excel_to_df(file_absolute_path):
        try:
            return pd.read_excel(file_absolute_path, sheet_name= 0, engine='xlrd')
        except:
            return pd.read_excel(file_absolute_path, sheet_name= 0, engine='openpyxl')