from .file_delete_service import FileDeleteService
from ...exceptions import *
from ..utils.utils import *
class TempDeleteService(FileDeleteService):
    @classmethod    
    def from_serializer(cls, serializer, user, status) -> "TempDeleteService":        
        file_object = serializer.get_temp_object(user, status)
        return cls(user, file_object)