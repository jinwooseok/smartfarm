from django.http import HttpResponse
import os
from ..utils.utils import *
from ...exceptions import *
class FileDownloadService:
    def __init__(self, file_name, file_root, content_type):
        self.file_name = file_name
        self.file_root = file_root
        self.content_type = content_type

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