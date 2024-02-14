from rest_framework import serializers
from ..file.serializers import FileNameSerializer
from ..file.repositorys import *
from ..file.exceptions.file_exception import FileNotFoundException
from ..models import File
class ProcessOutlierSerializer(FileNameSerializer):
    pass
    
class ProcessTimeSeriesSerializer(FileNameSerializer):
    windowSize = serializers.IntegerField()
    count = serializers.IntegerField()
    dateColumn = serializers.CharField()
    newFileName = serializers.CharField()
    feature = serializers.ListField(child=serializers.CharField())
    
    def get_temp_object_or_original(self, user,  status_id):
        file_objects = filter_file_by_user(user)
        temp_objects : Temp = Temp.objects.filter(file_title=self.data['fileName'], statuses=status_id)
        for file_object in file_objects:
            for temp_object in temp_objects:
                if file_object.id == temp_object.file_id:
                    return temp_object

class DataMergeSerializer(serializers.Serializer):
    mergeStandardVarList = serializers.JSONField()
    mergeDataNames = serializers.JSONField()
    
    def get_file_object_list(self, user):
        file_object_list = File.objects.filter(user=user, file_title__in=self.data['mergeDataNames'])
        return file_object_list