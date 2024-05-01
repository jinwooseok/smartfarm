from file.utils.utils import *
import pandas as pd
from file_data.utils.process import DataProcess
from get_file_data_service import GetFileDataService
from file.models import Temp

class GetTempDataService(GetFileDataService):
    def __init__(self, file_name, file_object, status_id):
        self.file_name = file_name
        self.file_object = file_object   
        self.status_id = status_id
        
    @classmethod
    def from_serializer(cls, serializer, user, status_id) -> 'GetTempDataService':
        file_object = serializer.get_file_object(user)
        file_name = file_object.file_title
        status_id = status_id
        return cls(file_name, file_object, status_id) 

    def execute(self):
        temp_object = self.get_temp_file(self.file_object.id, self.status_id)
        
        file_absolute_path = search_file_absolute_path(temp_object.file_root)
        dataFrame = self.file_to_df(file_absolute_path)
        
        data = DataProcess.round_converter(dataFrame)
        data = DataProcess.nan_to_string(data) 
        return DataProcess.df_to_json_object(data)
    
    @staticmethod
    def get_temp_file(file_id, status_id):
        try:
            instance = Temp.objects.get(file_id=file_id, statuses=status_id)
        except: instance = None
        
        return instance