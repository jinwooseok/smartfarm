from rest_framework import serializers
from ..models import FileFeature, ModelFeature
from ..file.serializers import FileNameSerializer
class FileFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileFeature
        fields = ['file','feature_order','feature_name','feature_type','feature_importance','feature_selected']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Modify the representation to change field names or exclude unnecessary fields
        representation['featureOrder'] = representation.pop('feature_order')
        representation['featureName'] = representation.pop('feature_name')
        representation['featureType'] = representation.pop('feature_type')
        representation['featureImportance'] = representation.pop('feature_importance')
        representation['featureSelected'] = representation.pop('feature_selected')
        return representation

class ModelFeatureSerializer(serializers.Serializer):
    class Meta:
        model = ModelFeature
        fields = ['model','feature_name','feature_type','weight']
        
class GetFeatureImportanceSerializer(FileNameSerializer):
    xValue = serializers.JSONField()
    yValue = serializers.CharField()
