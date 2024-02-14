from rest_framework import serializers
from ..file.serializers import FileNameSerializer
class FarmProcessSerializer(FileNameSerializer):
    newFileName = serializers.CharField()
    fileType = serializers.ChoiceField(choices=[("env","env"),("growth","growth"),("output","output")])
    startIndex = serializers.IntegerField()
    dateColumn = serializers.CharField()
    interval = serializers.ChoiceField(choices=[("daily","daily"),("weekly","weekly")])
    var = serializers.JSONField()

class EnvABMSSerializer(FileNameSerializer):
    newFileName = serializers.CharField()
    date = serializers.CharField()
    columns = serializers.JSONField()
    startIndex = serializers.IntegerField()