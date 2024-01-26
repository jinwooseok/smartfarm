from ...file_data.service.get_file_data_service import GetFileDataService
from ...file.utils.utils import search_file_absolute_path

class FarmProcessService():
    def __init__(self, farmProcessSerializer, fileNameSerializer, user):
        self.new_file_name = farmProcessSerializer.validated_data['newFileName']
        self.file_type = farmProcessSerializer.validated_data['fileType']
        self.start_index = farmProcessSerializer.validated_data['startIndex']
        self.date_column = farmProcessSerializer.validated_data['dateColumn']
        self.interval = farmProcessSerializer.validated_data['interval']
        self.file_root = fileNameSerializer.get_file_root(user)
        self.file_object = fileNameSerializer.get_file_object(user)
    
    def execute(self):
        file_absolute_path = search_file_absolute_path(self.file_root)
        df = GetFileDataService.file_to_df(file_absolute_path)
        return df

