import os
from ..exceptions.file_exception import *
from ..utils.utils import *
class FileDeleteService():    
    def __init__(self, serializer, user):
        self.user = user
        self.file_title = serializer.validated_data['fileName']
        self.file_root = serializer.get_file_root(user)
        self.file_object = serializer.get_file_object(user)

    def execute(self):
        file_absolute_path = search_file_absolute_path(self.file_root)
        #db제거
        self.file_object.delete()
        #파일제거
        try:
            os.remove(file_absolute_path)
        except:
            raise OriginalFileNotFoundException()