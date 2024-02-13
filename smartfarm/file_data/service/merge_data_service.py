from ...file.utils.utils import *
from .get_file_data_service import GetFileDataService
from ...file.service.temp_save_service import TempSaveService
from ..exceptions.file_data_exceptions import StandardDuplicateException
from ..utils.process import DataProcess

import pandas as pd

class MergeDataService():
    def __init__(self, user, file_object_list, column_name_list):
        self.user = user
        self.file_object_list = file_object_list
        self.column_name_list = column_name_list
        
    @classmethod    
    def from_serializer(cls, serializer, user):
        return cls(user
                    ,serializer.get_file_object_list(user)
                    ,serializer.validated_data['mergeStandardVarList'])
    
    def execute(self):
        dfs = []
        if len(self.file_object_list) == 1:
            file_object = self.file_object_list[0]
            file_absolute_path = search_file_absolute_path(file_object.file_root)
            df = GetFileDataService.file_to_df(file_absolute_path)
            dfs.append(df)
            
        else:   
            for i, file_object in enumerate(self.file_object_list):
                file_absolute_path = search_file_absolute_path(file_object.file_root)
                df = GetFileDataService.file_to_df(file_absolute_path)
                if df.duplicated(subset=self.column_name_list[i]).any():
                    raise StandardDuplicateException(file_object,self.column_name_list[i])
                df.rename(columns={self.column_name_list[i]:"기준"}, inplace=True)
                
                if type(df['기준']) is not object:
                    df['기준'] = df['기준'].astype('object')
                
                dfs.append(df)
                #메모리 제거
                del(df)
            
        merged_data = dfs[0]
    
        for i in range(1, len(dfs)):
            merged_data.info(memory_usage=True)
            merged_data = pd.merge(merged_data, dfs[i], on='기준', suffixes=(f'_{i}', f'_{i+1}'), how='outer', sort=True)
        
        file_title = self.new_file_name
        file_title = TempSaveService(self.user, file_title, merged_data, statuses=[4]).execute()
        
        return {file_title: DataProcess.df_to_json_object(merged_data)}

        