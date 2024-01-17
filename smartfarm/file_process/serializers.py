from rest_framework import serializers
from ..models import File
class FileSerializer(serializers.ModelSerializer):
    fileName = serializers.CharField(source='file_title')
    createdDate = serializers.DateTimeField(source='created_at')
    updatedDate = serializers.DateTimeField(source='updated_at')
    class Meta:
        model = File
        fields = ('file_title', 'created_at', 'updated_at')
    
    def success(self):
        return {"status":"success","message":"파일리스트 호출에 성공했습니다.","data":self.data}

class FileNameSerializer(serializers.ModelSerializer):
    fileName = serializers.CharField(source='file_title')
    class Meta:
        model = File
        fields = ('file_title',)
    
    def success(self):
        return {"status":"success","message":"파일명 호출에 성공했습니다.","data":self.data}

class FileSaveSerializer(serializers.Serializer):
    data = serializers.JSONField()