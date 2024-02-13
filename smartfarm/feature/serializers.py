from rest_framework import serializers
from ..models import FileFeature, ModelFeature
from ..file.serializers import FileNameSerializer
class FileFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileFeature
        fields = ['file','feature_order','feature_name','feature_type','feature_importance','feature_selected']
class ModelFeatureSerializer(serializers.Serializer):
    class Meta:
        model = ModelFeature
        fields = ['model','feature_name','feature_type','weight']
        
class GetFeatureImportanceSerializer(FileNameSerializer):
    xValue = serializers.JSONField()
    yValue = serializers.CharField()
