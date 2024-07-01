"""
사용자가 생성될 때마다 사용자의 디렉토리를 자동 생성
"""
import os
from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from users.models import User

@receiver(post_save, sender=User)
def create_directory(sender, instance, **kwargs):
    """
    사용자가 생성될 때마다 사용자의 디렉토리를 자동 생성
    만약 디렉토리가 이미 존재한다면 pass
    """
    try:
        os.makedirs(os.path.join(settings.MEDIA_ROOT, str(instance.id)))
    except:
        pass

    for dir in ['file', 'temp', 'model']:
        try:
            os.makedirs(os.path.join(settings.MEDIA_ROOT, str(instance.id), dir)) 
        except:
            pass