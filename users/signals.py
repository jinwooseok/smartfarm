from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from .models import User
import os
from django.conf import settings
@receiver(post_save, sender=User)
def create_directory(sender, instance, **kwargs):
    # 사용자가 생성될 때마다 사용자의 디렉토리를 생성
    try:
        os.makedirs(os.path.join(settings.MEDIA_ROOT, str(instance.id)))
    except:
        pass
    
    for dir in ['file', 'temp', 'model']:
        try:
            os.makedirs(os.path.join(settings.MEDIA_ROOT, str(instance.id), dir)) 
        except:
            pass