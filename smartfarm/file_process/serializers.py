from rest_framework import serializers
from ..models import File

class FileInfoSerializer(serializers.ModelSerializer):
    fileName = serializers.CharField(source='file_title')
    createdDate = serializers.DateTimeField(source='created_at')
    updatedDate = serializers.DateTimeField(source='updated_at')
    class Meta:
        model = File
        fields = ['fileName', 'createdDate', 'updatedDate']


class FileNameSerializer(serializers.ModelSerializer):
    fileName = serializers.CharField(source='file_title')
    class Meta:
        model = File
        fields = ('fileName',)
    
    def get_file_root(self):
        file_object = File.objects.get(file_title=self.validated_data['fileName'])
        file_root = file_object.file_root
        return file_root
        

class FileSaveSerializer(serializers.Serializer):
    fileName = serializers.CharField()
    fileData = serializers.JSONField()

class FileDeleteSerializer(serializers.Serializer):
    fileName = serializers.JSONField()