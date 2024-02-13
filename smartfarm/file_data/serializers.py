from rest_framework import serializers
from ..file.serializers import FileNameSerializer
from ..file.exceptions.file_exception import FileNotFoundException
from ..models import File
class ProcessOutlierSerializer(FileNameSerializer):
    pass
    
class ProcessTimeSeriesSerializer(FileNameSerializer):
    windowSize = serializers.IntegerField()
    count = serializers.IntegerField()
    dateColumn = serializers.IntegerField()
    newFileName = serializers.CharField()
    feature = serializers.JSONField()

class DataMergeSerializer(serializers.Serializer):
    mergeStandardVarList = serializers.JSONField()
    mergeDataNames = serializers.JSONField()
    
    def get_file_object_list(self, user):
        file_object_list = File.objects.filter(user=user, file_title__in=self.data['mergeDataNames'])
        if len(file_object_list) != len(self.data['mergeDataNames']):
            raise FileNotFoundException()
        return file_object_list