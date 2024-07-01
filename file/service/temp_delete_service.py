"""
file delete service를 상속받아 temp file delete service를 구현. 임시 파일을 삭제하는 서비스
"""
from file.service.file_delete_service import FileDeleteService
from common.exceptions import *
from file.utils.utils import *
class TempDeleteService(FileDeleteService):
    @classmethod    
    def from_serializer(cls, serializer, user, status) -> "TempDeleteService":        
        file_object = serializer.get_temp_object(user, status)
        return cls(user, file_object)