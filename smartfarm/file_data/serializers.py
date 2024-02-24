from rest_framework import serializers
from ..file.serializers import FileNameSerializer
from ..file.repositorys import *
from ..exceptions import *

class ProcessOutlierSerializer(FileNameSerializer):
    pass
    
class ProcessTimeSeriesSerializer(FileNameSerializer):
    count = serializers.IntegerField()
    xValue = serializers.JSONField()
    yValue = serializers.CharField()
    
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
        file_object_list = []
        for file_title in self.data['mergeDataNames']:
            file_object_list.append(get_file_by_user_file_title(user, file_title))
        return file_object_list