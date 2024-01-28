from ...file_data.service.get_file_data_service import GetFileDataService
from ...file.utils.utils import search_file_absolute_path

class FarmProcessService():
    def __init__(self, serializer, user):
        self.new_file_name = serializer.validated_data['newFileName']
        self.file_type = serializer.validated_data['fileType']
        self.start_index = serializer.validated_data['startIndex']
        self.date_column = serializer.validated_data['dateColumn']
        self.interval = serializer.validated_data['interval']
        self.file_root = serializer.get_file_root(user)
        self.file_object = serializer.get_file_object(user)
    
    def execute(self):
        file_absolute_path = search_file_absolute_path(self.file_root)
        df = GetFileDataService.file_to_df(file_absolute_path)
        
        return df

