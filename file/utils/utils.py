import os
def search_file_absolute_path(file_root):
        from django.conf import settings
        return os.path.join(settings.MEDIA_ROOT, str(file_root))