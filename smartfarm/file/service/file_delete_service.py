from ...exceptions import *
from ..utils.utils import *
from ...models import *
class FileDeleteService():    
    def __init__(self, user, file_object):
        self.user = user
        self.file_object = file_object
        self.file_root = file_object.file_root
    
    @classmethod    
    def from_serializer(cls, serializer, user) -> "FileDeleteService":        
        file_object = serializer.get_file_object(user)
        return cls(user, file_object)
    
        
    def execute(self):
        #db상 파일 제거
        self.file_object.delete()