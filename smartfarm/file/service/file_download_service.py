from django.http import HttpResponse
import os
from django.conf import settings
from ..utils.utils import *
from ..exceptions.file_exception import *
class FileDownloadService:
    
    def __init__(self, serializer, user):
        self.file_name = serializer.data['fileName']
        self.file_root = serializer.get_file_object(user).file_root
    
    def from_serializer(cls, serializer, user) -> 'FileDownloadService':
        file_name = serializer.data['fileName']
        file_root = serializer.get_file_object(user).file_root
        return cls(serializer, user)
    
    def execute(self):
        file_absolute_path = search_file_absolute_path(self.file_root)
        return self.attach_file(self.file_name, file_absolute_path)

    @staticmethod
    def attach_file(file_name, file_path):
        if os.path.exists(file_path):
            response = HttpResponse(open(file_path, 'rb'), content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=' + file_name
            return response
        else:
            raise FileNotFoundException()