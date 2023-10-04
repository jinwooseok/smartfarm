from django.db import models
from users.models import User
import os
from config import settings
# Create your models here.
class File(models.Model):
    file_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,default=000000)
    file_type = models.CharField(max_length=200,blank=True)
    file_title = models.CharField(max_length=200)
    file_root = models.FileField(upload_to='file/<user_id>')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    