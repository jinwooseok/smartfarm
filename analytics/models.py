"""
학습된 모델, 모델 메타 정보를 저장하는 모델
"""
import os
import pickle
import json
from django.conf import settings
from django.db import models
from users.models import User

# Create your models here.
def user_model_path(instance, file_root):
    """
    파일이 저장될 경로: media/<user_id>/model/<filename>
    """
    return f"{instance.user.id}/model/{file_root}"


class LearnedModel(models.Model):
    """
    학습된 모델, 모델 메타 정보를 저장하는 모델
    
    user : 사용자 정보, User모델과 연결된 외래키, User모델이 삭제되면 함께 삭제된다.
    original_file_name : 만들어진 모델의 원본 파일명
    model_name : 모델 파일명
    model_root : 모델 파일이 저장된 경로
    model_meta_name : 모델 메타 정보 파일명
    model_meta_root : 모델 메타 정보 파일이 저장된 경로
    created_at : 생성일자
    updated_at : 수정일자    
    """
    user = models.ForeignKey(User,on_delete=models.CASCADE,default=000000)
    original_file_name = models.CharField(max_length=200, default=None)
    model_name = models.CharField(max_length=200, default=None)
    model_root = models.CharField(max_length=200, default=None)
    model_meta_name = models.CharField(max_length=200, default=None)
    model_meta_root = models.CharField(max_length=200, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, model, model_meta : dict, *args, **kwargs):
        """
        모델을 저장하는 함수
        """
        self.model_root = self.get_model_file_path()
        self.model_meta_root = self.get_model_meta_file_path()
        with open(self.model_root, 'wb') as f:
            pickle.dump(model, f)
        with open(self.model_meta_root, 'w', encoding='utf-8') as f:
            json.dump(model_meta, f, ensure_ascii=False)
        super().save(*args, **kwargs)

    def get_model_file_path(self):
        """
        모델 파일이 저장될 경로 반환
        """
        return os.path.join(settings.MEDIA_ROOT, user_model_path(self, self.model_name))

    def get_model_meta_file_path(self):
        """
        모델 메타정보 파일이 저장될 경로 반환
        """
        return os.path.join(settings.MEDIA_ROOT, user_model_path(self, self.model_meta_name))
    