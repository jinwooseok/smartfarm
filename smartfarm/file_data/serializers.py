from rest_framework import serializers
from ..file.serializers import FileNameSerializer

class ProcessOutlierSerializer(FileNameSerializer):
    pass
    
class ProcessTimeSeriesSerializer(FileNameSerializer):
    windowSize = serializers.IntegerField()