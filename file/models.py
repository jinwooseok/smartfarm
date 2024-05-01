from django.db import models

# Create your models here.
def user_file_path(instance, file_root):
    # 파일이 저장될 경로: media/file/<user_id>/<filename>
    return '{0}/file/{1}'.format(instance.user.id, file_root)

def user_temp_path(instance, file_root):
    # 파일이 저장될 경로: media/file/<user_id>/<filename>
    return '{0}/temp/{1}'.format(instance.file.user.id, file_root)

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