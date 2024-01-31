from rest_framework import serializers
from ..models import File, Temp
from .exceptions.file_exception import FileNotFoundException
class FileInfoSerializer(serializers.ModelSerializer):
    fileName = serializers.CharField(source='file_title')
    createdDate = serializers.DateTimeField(source='created_at', format='%Y-%m-%d')
    updatedDate = serializers.DateTimeField(source='updated_at', format='%Y-%m-%d')
    class Meta:
        model = File
        fields = ['fileName', 'createdDate', 'updatedDate']


class FileNameModelSerializer(serializers.ModelSerializer):
    fileName = serializers.CharField(source='file_title')
    class Meta:
        model = File
        fields = ('fileName',)
    
    def get_file_object(self, user):
            try:
                return File.objects.get(user=user, file_title=self.data['fileName'])
            except:
                raise FileNotFoundException()
            
class FileNameSerializer(serializers.Serializer):
    fileName = serializers.CharField()
    
    def get_file_object(self, user):
        try:
            return File.objects.get(user=user, file_title=self.data['fileName'])
        except:
            raise FileNotFoundException()
    
    def get_temp_object(self, user, status_id):
        try:
            file_object = self.get_file_object(user)
            file_id = file_object.id
            return Temp.objects.get(file_id=file_id, statuses=status_id)
        except:
            raise FileNotFoundException()
        

class FileSaveSerializer(FileNameSerializer):
    fileData = serializers.JSONField()


class FileDeleteSerializer(FileNameSerializer):
    fileName = serializers.JSONField()