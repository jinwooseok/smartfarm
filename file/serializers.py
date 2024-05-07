from rest_framework import serializers
from file.models import File, Temp
from file.repositorys import (get_file_by_user_file_title,
                              get_temp_by_file_id_status_id,
                              get_temp_or_none_by_file_id_status_id)
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
    
    def get_file_object(self, user)->File:
        return get_file_by_user_file_title(user, self.data['fileName'])
            
class FileNameSerializer(serializers.Serializer):
    fileName = serializers.CharField()
    
    def get_file_object(self, user)->File:
        return get_file_by_user_file_title(user, self.data['fileName'])
    
    def get_temp_object(self, user, status_id)->Temp:
        file_object = self.get_file_object(user)
        file_id = file_object.id
        return get_temp_by_file_id_status_id(file_id, status_id)
    
    def get_temp_object_or_none(self, user, status_id):
        file_object = self.get_file_object(user)
        file_id = file_object.id
        return get_temp_or_none_by_file_id_status_id(file_id, status_id)
        
    def get_temp_object_or_original(self, user, status_id):
        file_object = self.get_file_object(user)
        file_id = file_object.id
        if get_temp_or_none_by_file_id_status_id(file_id, status_id) is None:
            return file_object
        return get_temp_by_file_id_status_id(file_id, status_id)

class FileSaveSerializer(FileNameSerializer):
    fileData = serializers.JSONField()
    dateColumn = serializers.CharField(allow_null=True, default=None, required=False)
    startIndex = serializers.IntegerField(allow_null=True, default=1, required=False)


class FileDeleteSerializer(FileNameSerializer):
    fileName = serializers.JSONField()