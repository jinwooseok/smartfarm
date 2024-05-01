from django.apps import AppConfig


class FileConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'file'
    
    def ready(self):
        from .file.utils import signals  # 시그널 파일을 임포트합니다.
        from . import scheduler
        scheduler.start()
