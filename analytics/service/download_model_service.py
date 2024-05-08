"""
DB와 파일 시스템에 저장된 모델을 사용자가 다운로드하는 서비스를 제공하는 파일
"""
from file.service.file_download_service import FileDownloadService

class DownloadModelService(FileDownloadService):
    """
    설명
    - 모델 다운로드 서비스로 FileDownloadService를 상속받아 구현
    """
    @classmethod
    def from_serializer(cls, serializer, user):
        """
        설명
        - serializer를 통해 모델 정보를 받아와 ModelDownloadService 객체를 생성하는 메서드
        """
        model_object = serializer.get_model_object(user)
        return cls(
            model_object.model_name
            ,model_object.model_root
            ,'application/octet-stream')
