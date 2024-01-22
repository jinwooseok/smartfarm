import os
from ..exceptions.file_exception import *
from ..utils.utils import *
from ...models import *
class FileDeleteService():    
    def __init__(self, serializer, user):
        self.user = user
        self.file_title = serializer.validated_data['fileName']
        self.file_root = serializer.get_file_root(user)
        self.file_object = serializer.get_file_object(user)

    def execute(self):
        file_absolute_path = search_file_absolute_path(self.file_root)
        #관련 변수 제거
        Feature.objects.filter(file_id=self.file_object.id).delete()
        #db상 파일 제거
        self.file_object.delete()
        file_absolute_path = search_file_absolute_path(self.file_root)
        #실제 파일 제거
        FileDeleteService.delete_local_file(file_absolute_path)

    
    @staticmethod
    def delete_local_file(file_path):
        try:
            os.remove(file_path)
        except:
            raise OriginalFileNotFoundException()