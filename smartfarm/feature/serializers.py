from rest_framework import serializers
from ..models import FileFeature

class FileFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileFeature
        fields = ['file','feature_order','feature_name','feature_type','feature_importance','feature_selected']