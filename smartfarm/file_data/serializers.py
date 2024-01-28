from rest_framework import serializers
from ..file.serializers import FileNameSerializer

class ProcessOutlierSerializer(FileNameSerializer):
    newFileName = serializers.CharField()