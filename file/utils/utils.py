import os
def search_file_absolute_path(file_root):
        """
        파일의 절대 경로를 찾음
        """
        from django.conf import settings
        return os.path.join(settings.MEDIA_ROOT, str(file_root))