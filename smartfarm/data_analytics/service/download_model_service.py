from ...file.service.file_download_service import FileDownloadService

class DownloadModelService(FileDownloadService):
    @classmethod
    def from_serializer(cls, serializer, user):
        model_object = serializer.get_model_object(user)
        return cls(
            model_object.model_name
            ,model_object.model_root
            ,'application/octet-stream')