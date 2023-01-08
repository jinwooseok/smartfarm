from django.db import models
from users.models import User
# Create your models here.
class File_db(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,default=000000)
    file_type = models.CharField(max_length=200,blank=True)
    file_Title = models.CharField(max_length=200)
    file_Root = models.FileField(upload_to='file/%Y/%m/%d/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)