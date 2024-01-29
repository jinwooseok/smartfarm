from rest_framework import serializers
from ..file.serializers import FileNameSerializer
class FarmProcessSerializer(FileNameSerializer):
    newFileName = serializers.CharField()
    fileType = serializers.ChoiceField(choices=[("env","env"),("growth","growth"),("output","output")])
    startIndex = serializers.IntegerField()
    dateColumn = serializers.IntegerField()
    interval = serializers.ChoiceField(choices=[("daily","daily"),("weekly","weekly")])
    var = serializers.ListField()
