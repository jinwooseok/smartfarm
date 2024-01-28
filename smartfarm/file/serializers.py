from rest_framework import serializers
from ..models import File
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
    
    def get_file_root(self, user):
        try:
            print(user, self.data['fileName'])
            file_object = File.objects.get(user=user, file_title=self.data['fileName'])
        except:
            raise FileNotFoundException()
        
        return file_object.file_root
    
    def get_file_object(self, user):
        try:
            return File.objects.get(user=user, file_title=self.data['fileName'])
        except:
            raise FileNotFoundException()
        
class FileNameSerializer(serializers.Serializer):
    fileName = serializers.CharField()
    
    def get_file_root(self, user):
        try:
            print(user, self.data['fileName'])
            file_object = File.objects.get(user=user, file_title=self.data['fileName'])
        except:
            raise FileNotFoundException()
        
        return file_object.file_root
    
    def get_file_object(self, user):
        try:
            return File.objects.get(user=user, file_title=self.data['fileName'])
        except:
            raise FileNotFoundException()
        

class FileSaveSerializer(FileNameSerializer):
    fileData = serializers.JSONField()


class FileDeleteSerializer(FileNameSerializer):
    fileName = serializers.JSONField()