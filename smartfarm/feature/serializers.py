from rest_framework import serializers
from ..models import Feature

class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ['file','feature_order','feature_name','feature_type','feature_importance','feature_selected']