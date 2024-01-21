from django.http import HttpResponse, JsonResponse
import os
from django.conf import settings
from ...models import File

class FileDownloadService:
    
    def __init__(self, serializer):
        self.file_name = serializer.validated_data['fileName']
        self.file_path = os.path.join(settings.MEDIA_ROOT, serializer.get_file_root())
    
    def execute(self):
        print(self.file_path)
        return self.attach_file(self.file_name, self.file_path)

    @staticmethod
    def attach_file(file_name, file_path):
        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                response = HttpResponse(file.read())
                response['Content-Disposition'] = 'attachment; filename="{}"'.format(file_name)
                return response