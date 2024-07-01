"""
파일 저장과 삭제에 대한 시그널을 처리하는 파일
"""
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
import os
from file.models import File, Temp
from file.utils.utils import search_file_absolute_path
from feature.service.feature_service import FeatureService
from feature.serializers import FileFeatureSerializer
from common.validators import serializer_validator
from common.exceptions import *

@receiver(pre_delete, sender=File)
def delete_file(sender, instance, **kwargs):
    """
    DB 상 파일 삭제 시 파일 시스템 상 파일도 삭제
    """
    delete_local_file(search_file_absolute_path(instance.file_root))
    
@receiver(pre_delete, sender=Temp)
def delete_temp(sender, instance, **kwargs):
    """
    DB 상 파일 삭제 시 파일 시스템 상 파일도 삭제
    """
    delete_local_file(search_file_absolute_path(instance.file_root))
    
def delete_local_file(file_path):
    """
    파일 시스템 상 파일 삭제
    """
    try:
        os.remove(search_file_absolute_path(file_path))
    except:
        raise OriginalFileNotFoundException()
    
@receiver(post_save, sender=File)
def create_file(sender, instance, **kwargs):
    """
    파일 저장 시 변수도 동시에 저장
    """
    feature_info_list = FeatureService.extract_feature(instance)
    #변수 정보 저장
    feature_serializer = FileFeatureSerializer(data=feature_info_list, many=True)
    feature_serializer = serializer_validator(feature_serializer)
    feature_serializer.save()