from django.db import models
from users.models import User

# Create your models here.
def user_media_path(instance, file_root):
    # 파일이 저장될 경로: media/file/<user_id>/<filename>
    return 'file/{0}/{1}'.format(instance.user_id.id, file_root)

class File(models.Model):
    file_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,default=000000)
    file_type = models.CharField(max_length=200,blank=True)
    file_title = models.CharField(max_length=200)
    file_root = models.FileField(upload_to=user_media_path,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
