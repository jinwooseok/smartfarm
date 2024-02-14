from rest_framework import serializers
from ..file.serializers import FileNameSerializer
class FarmProcessSerializer(FileNameSerializer):
    newFileName = serializers.CharField()
    fileType = serializers.ChoiceField(choices=[("env","env"),("growth","growth"),("output","output")])
    interval = serializers.ChoiceField(choices=[("daily","daily"),("weekly","weekly")])
    var = serializers.JSONField()

class EnvABMSSerializer(FileNameSerializer):
    newFileName = serializers.CharField()
    columns = serializers.JSONField()