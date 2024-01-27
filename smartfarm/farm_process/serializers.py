from rest_framework import serializers
class FarmProcessSerializer(serializers.Serializer):
    newFileName = serializers.CharField()
    fileType = serializers.ChoiceField(choices=[("envir","envir"),("growth","growth"),("output","output")])
    startIndex = serializers.IntegerField()
    dateColumn = serializers.IntegerField()
    interval = serializers.ChoiceField(choices=[("daily","daily"),("weekly","weekly")])
    
