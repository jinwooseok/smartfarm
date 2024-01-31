from django.db.models.signals import pre_delete
from django.dispatch import receiver
from ...models import File, Temp
import os
from ..exceptions.file_exception import *
from ..utils.utils import *

@receiver(pre_delete, sender=File)
def delete_file(sender, instance, **kwargs):
    print(instance)
    delete_local_file(search_file_absolute_path(instance.file_root))
    
@receiver(pre_delete, sender=Temp)
def delete_temp(sender, instance, **kwargs):
    print(instance)
    delete_local_file(search_file_absolute_path(instance.file_root))
    

def delete_local_file(file_path):
    try:
        os.remove(search_file_absolute_path(file_path))
    except:
        raise OriginalFileNotFoundException()