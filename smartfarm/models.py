from django.db import models
from users.models import User

# Create your models here.
def user_file_path(instance, file_root):
    # 파일이 저장될 경로: media/file/<user_id>/<filename>
    return '{0}/file/{1}'.format(instance.user.id, file_root)

def user_model_path(instance, file_root):
    # 파일이 저장될 경로: media/file/<user_id>/<filename>
    return '{0}/model/{1}'.format(instance.user.id, file_root)

class File(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,default=000000)
    file_type = models.CharField(max_length=200,null=True)
    file_title = models.CharField(max_length=200)
    file_root = models.FileField(upload_to=user_file_path,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    statuses = models.ManyToManyField('StatusCode', through='Status')

class StatusCode(models.Model):
    status_id = models.IntegerField(null=False)
    status_name = models.CharField(max_length=200, null=False)

class Status(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    status = models.ForeignKey(StatusCode, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Feature(models.Model):
    file = models.ForeignKey(File,on_delete=models.CASCADE,default=000000)
    feature_order = models.IntegerField()
    feature_name = models.CharField(max_length=200)
    feature_type = models.CharField(max_length=200)
    feature_importance = models.FloatField(null=True)
    feature_selected = models.BooleanField(default=False)

class LearnedModel(models.Model):
    file = models.ForeignKey(File,on_delete=models.CASCADE,default=000000)
    model_name = models.CharField(max_length=200)
    model_meta_root = models.FileField(upload_to=user_model_path, max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ModelFeature(models.Model):
    model = models.ForeignKey(LearnedModel,on_delete=models.CASCADE,default=000000)
    feature_order = models.IntegerField()
    feature_name = models.CharField(max_length=200)
    weight = models.FloatField(null=True)