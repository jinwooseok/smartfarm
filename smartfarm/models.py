from django.db import models
from users.models import User

# Create your models here.
def user_media_path(instance, file_root):
    # 파일이 저장될 경로: media/file/<user_id>/<filename>
    return 'file/{0}/{1}'.format(instance.user_id.id, file_root)

class File(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,default=000000)
    file_type = models.CharField(max_length=200,null=True)
    file_title = models.CharField(max_length=200)
    file_root = models.FileField(upload_to=user_media_path,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.ManyToManyField('Status', through='Status', related_name='file_status')

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
    model_meta_root = models.CharField(max_length=200)
    model_weight_root = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)