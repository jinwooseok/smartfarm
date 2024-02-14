from django.db import models
from users.models import User
import os
import pickle
from django.conf import settings
import json

# Create your models here.
def user_file_path(instance, file_root):
    # 파일이 저장될 경로: media/file/<user_id>/<filename>
    return '{0}/file/{1}'.format(instance.user.id, file_root)

def user_temp_path(instance, file_root):
    # 파일이 저장될 경로: media/file/<user_id>/<filename>
    return '{0}/temp/{1}'.format(instance.file.user.id, file_root)

def user_model_path(instance, file_root):
    # 파일이 저장될 경로: media/file/<user_id>/<filename>
    return '{0}/model/{1}'.format(instance.user.id, file_root)

class File(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,default=000000)
    file_type = models.CharField(max_length=200,null=True)
    file_title = models.CharField(max_length=200)
    file_root = models.FileField(upload_to=user_file_path,null=True)
    date_column = models.CharField(max_length=200,null=True)
    start_index = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    statuses = models.ManyToManyField('FileStatusCode', through='FileStatus')

class FileStatusCode(models.Model):
    status_name = models.CharField(max_length=200, null=False)

class FileStatus(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    status = models.ForeignKey(FileStatusCode, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
class FileFeature(models.Model):
    file = models.ForeignKey(File,on_delete=models.CASCADE,default=000000)
    feature_order = models.IntegerField()
    feature_name = models.CharField(max_length=200)
    feature_type = models.CharField(max_length=200)
    feature_importance = models.FloatField(null=True)
    feature_selected = models.BooleanField(default=False)

class Temp(models.Model):
    file = models.ForeignKey(File,on_delete=models.CASCADE,default=000000)
    file_type = models.CharField(max_length=200,null=True)
    file_title = models.CharField(max_length=200)
    file_root = models.FileField(upload_to=user_temp_path,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    statuses = models.ManyToManyField('TempStatusCode', through='TempStatus')

class TempStatusCode(models.Model):
    status_name = models.CharField(max_length=200, null=False)

class TempStatus(models.Model):
    temp = models.ForeignKey(Temp, on_delete=models.CASCADE)
    status = models.ForeignKey(TempStatusCode, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
class TempFeature(models.Model):
    temp = models.ForeignKey(Temp,on_delete=models.CASCADE,default=000000)
    feature_order = models.IntegerField()
    feature_name = models.CharField(max_length=200)
    feature_type = models.CharField(max_length=200)
    feature_importance = models.FloatField(null=True)
    feature_selected = models.BooleanField(default=False)

class LearnedModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,default=000000)
    original_file_name = models.CharField(max_length=200, default=None)
    model_name = models.CharField(max_length=200, default=None)
    model_root = models.CharField(max_length=200, default=None)
    model_meta_name = models.CharField(max_length=200, default=None)
    model_meta_root = models.CharField(max_length=200, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, model, model_meta : dict, *args, **kwargs):
        # joblib.dump를 사용하여 파일 저장
        self.model_root = self.get_model_file_path()
        self.model_meta_root = self.get_model_meta_file_path()
        if model_meta['model_name'] == 'Linear Regression':
            model.save(self.model_root)
        else:
            with open(self.model_root, 'w') as f:
                pickle.dump(model, f)
        with open(self.model_meta_root, 'w') as f:
            json.dump(model_meta, f, ensure_ascii=False)
        super().save(*args, **kwargs)

    def get_model_file_path(self):
        # 파일이 저장될 경로 반환
        return os.path.join(settings.MEDIA_ROOT, user_model_path(self, self.model_name))
    
    def get_model_meta_file_path(self):
        # 파일이 저장될 경로 반환
        return os.path.join(settings.MEDIA_ROOT, user_model_path(self, self.model_meta_name))

class ModelFeature(models.Model):
    model = models.ForeignKey(LearnedModel,on_delete=models.CASCADE,default=000000)
    feature_name = models.CharField(max_length=200)
    feature_type = models.Choices('feature','target')
    weight = models.FloatField(null=True)