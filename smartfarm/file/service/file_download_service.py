from django.http import FileResponse
import os
from django.conf import settings
from ..utils.utils import *
from ..exceptions.file_exception import *
class FileDownloadService:
    
    def __init__(self, serializer, user):
        self.file_name = serializer.data['fileName']
        self.file_root = serializer.get_file_root(user)
    
    def execute(self):
        file_absolute_path = search_file_absolute_path(self.file_root)
        return self.attach_file(self.file_name, file_absolute_path)

    @staticmethod
    def attach_file(file_name, file_path):
        if os.path.exists(file_path):
            return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=file_name, content_type='application/octet-stream')
        else:
            raise FileNotFoundException()