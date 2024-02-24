from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from ...models import File, Temp, LearnedModel
import os
from ...exceptions import *
from ..utils.utils import *
from ...feature.service.feature_service import FeatureService
from ...feature.serializers import FileFeatureSerializer
from common.validators import serializer_validator

@receiver(pre_delete, sender=File)
def delete_file(sender, instance, **kwargs):
    delete_local_file(search_file_absolute_path(instance.file_root))
    
@receiver(pre_delete, sender=Temp)
def delete_temp(sender, instance, **kwargs):
    delete_local_file(search_file_absolute_path(instance.file_root))
    
@receiver(pre_delete, sender=LearnedModel)
def delete_file(sender, instance, **kwargs):
    delete_local_file(search_file_absolute_path(instance.model_root))
    delete_local_file(search_file_absolute_path(instance.model_meta_root))
    
def delete_local_file(file_path):
    try:
        os.remove(search_file_absolute_path(file_path))
    except:
        raise OriginalFileNotFoundException()
    
@receiver(post_save, sender=File)
def create_file(sender, instance, **kwargs):
    feature_info_list = FeatureService.extract_feature(instance)
    #변수 정보 저장
    feature_serializer = FileFeatureSerializer(data=feature_info_list, many=True)
    feature_serializer = serializer_validator(feature_serializer)
    
    feature_serializer.save()