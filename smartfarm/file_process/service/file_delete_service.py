from ...models import File
import os
from ..exceptions.file_exception import *

class FileSaveService():    
    def __init__(self, serializer, user):
        self.user = user
        self.file_title = serializer.validated_data['fileName']

    def excute(self):
        file_object = File.objects.filter(self.user, self.file_title)
        
        if file_object is None:
            raise FileNotFoundException()

        file_absolute_path = self.search_file_absolute_path(file_object.file_root)
        #db제거
        file_object.delete()
        #파일제거
        try:
            os.remove(file_absolute_path)
        except:
            raise OriginalFileNotFoundException()
    
    def search_file_absolute_path(file_root):
        from django.conf import settings
        return os.path.join(settings.MEDIA_ROOT, str(file_root))