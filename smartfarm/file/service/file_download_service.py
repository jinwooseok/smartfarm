from django.http import HttpResponse
import os
from django.conf import settings
from ..utils.utils import *
from ..exceptions.file_exception import *
class FileDownloadService:
    
    def __init__(self, serializer, user):
        self.file_name = serializer.data['fileName']
        self.file_root = serializer.get_file_object(user).file_root
        self.content_type = 'text/csv'
    def execute(self):
        file_absolute_path = search_file_absolute_path(self.file_root)
        return self.attach_file(file_absolute_path)

    def attach_file(self, file_path):
        if os.path.exists(file_path):
            response = HttpResponse(open(file_path, 'rb'), content_type=self.content_type)
            response['Content-Disposition'] = 'attachment; filename=' + self.file_name
            return response
        else:
            raise FileNotFoundException()