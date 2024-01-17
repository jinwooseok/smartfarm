from django.db import models
from users.models import User

# Create your models here.
def user_media_path(instance, file_root):
    # 파일이 저장될 경로: media/file/<user_id>/<filename>
    return 'file/{0}/{1}'.format(instance.user_id.id, file_root)

class File(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,default=000000)
    file_type = models.CharField(max_length=200,blank=True)
    file_title = models.CharField(max_length=200)
    file_root = models.FileField(upload_to=user_media_path,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Status(models.Model):
    file = models.ForeignKey(File,on_delete=models.CASCADE,default=000000)
    status_id = models.IntegerChoices('status_id','0 1 2 3 4 5 6 7 8 9')
    status_name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

class StatusCode(models.Model):
    status_name = models.CharField(max_length=200)

class Feature(models.Model):
    file = models.ForeignKey(File,on_delete=models.CASCADE,default=000000)
    feature_order = models.IntegerField()
    feature_name = models.CharField(max_length=200)
    feature_type = models.CharField(max_length=200)
    feature_importance = models.FloatField()
    feature_selected = models.BooleanField(default=False)

class LearnedModel(models.Model):
    file = models.ForeignKey(File,on_delete=models.CASCADE,default=000000)
    model_name = models.CharField(max_length=200)
    model_type = models.CharField(max_length=200)
    model_score = models.FloatField()
    model_params = models.CharField(max_length=200)
    model_status = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)