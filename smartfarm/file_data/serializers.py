from rest_framework import serializers
from ..file.serializers import FileNameSerializer
from ..file.exceptions.file_exception import FileNotFoundException
from ..models import File
class ProcessOutlierSerializer(FileNameSerializer):
    pass
    
class ProcessTimeSeriesSerializer(FileNameSerializer):
    windowSize = serializers.IntegerField()

class DataMergeSerializer(serializers.Serializer):
    fileName = serializers.ListField()
    columnName = serializers.ListField()
    
    def get_file_object_list(self, user):
        file_object_list = File.objects.filter(user=user, file_title__in=self.data['fileName'])
        if len(file_object_list) != len(self.data['fileName']):
            raise FileNotFoundException()
        return file_object_list