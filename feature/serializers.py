"""
변수 저장과 표현에 대한 정의를 포함하는 파일입니다.
"""
from rest_framework import serializers
from feature.models import FileFeature, ModelFeature
from file.serializers import FileNameSerializer
class FileFeatureSerializer(serializers.ModelSerializer):
    """
    FileFeature 모델에 대한 Serializer
    
    Attributes
    ----------
    file : File
        파일 인스턴스
    feature_order : int
        feature 순서
    feature_name : str
        feature 이름
    feature_type : str
        feature 타입
    feature_importance : float
        feature 중요도
    feature_selected : bool
        feature 선택 여부
    """
    class Meta:
        model = FileFeature
        fields = ['file','feature_order','feature_name','feature_type','feature_importance','feature_selected']

    def to_representation(self, instance):
        """
        FileFeature 모델의 표현을 변경하여 반환
        DB 형식에서 API 형식으로 변환
        """
        representation = super().to_representation(instance)
        # Modify the representation to change field names or exclude unnecessary fields
        representation['featureOrder'] = representation.pop('feature_order')
        representation['featureName'] = representation.pop('feature_name')
        representation['featureType'] = representation.pop('feature_type')
        feature_importance = representation['feature_importance']
        if feature_importance is not None:
            representation['featureImportance'] = round(feature_importance, 2)
        representation['featureSelected'] = representation.pop('feature_selected')
        
        return representation

class ModelFeatureSerializer(serializers.ModelSerializer):
    """
    ModelFeature 모델에 대한 Serializer
    """
    class Meta:
        model = ModelFeature
        fields = ['model','feature_name','feature_type','weight']

class GetFeatureImportanceSerializer(FileNameSerializer):
    """
    변수 중요도를 계산하기 위한 Serializer
    """
    xValue = serializers.JSONField()
    yValue = serializers.CharField()
    fileData = serializers.JSONField()
