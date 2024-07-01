"""
변수 중요도를 계산하는 서비스
"""
import pandas as pd
import numpy as np
from feature.serializers import GetFeatureImportanceSerializer
from analytics.utils.correlation import calculate_correlation
from common.exceptions import *
class FeatureImportanceService:
    """
    변수 중요도를 계산하는 서비스
    
    메서드
    __init__ : 변수 중요도를 계산하기 위한 초기화
    from_serializer : serializer로부터 데이터를 가져와 객체를 생성
    execute : 변수 중요도를 계산하여 반환
    importance_form : 변수 중요도를 반환하기 위한 형식
    """
    def __init__(self, x_value, y_value, data):
        self.x_value = x_value
        self.y_value = y_value
        self.data = data
    
    @classmethod
    def from_serializer(cls, serializer: GetFeatureImportanceSerializer, user):
        return cls(serializer.validated_data['xValue']
                   ,serializer.validated_data['yValue']
                   ,serializer.validated_data['fileData'])

    def execute(self):
        """
        변수 중요도를 계산하여 반환
        
        로직 
        1. 데이터를 DataFrame으로 변환
        2. x_value, y_value가 데이터에 있는지 확인
        3. 데이터의 빈 값을 nan으로 변환
        4. y_value에 대한 각 변수 중요도를 계산하여 반환
        """
        df = pd.DataFrame(self.data)
        for name in self.x_value+[self.y_value]:
            if name not in df.columns:
                raise InvalidFeatureException(name)
        # 데이터의 빈 값을 nan으로 변환
        df.replace('', np.nan, inplace=True)
        response = []
        # y_value에 대한 각 변수 중요도를 계산하여 반환(상관 계수 계산(calculate_correlation))
        for idx, name in enumerate(self.x_value):
            feature_importance = calculate_correlation(df, name, self.y_value)
            if feature_importance is not None and np.isnan(feature_importance):
                feature_importance = 'nan'
            elif feature_importance is not None and np.isfinite(feature_importance)!=True:
                feature_importance = 'inf'
            form = self.importance_form(idx, name, str(df[name].dtype), feature_importance)
            response.append(form)
        return response

    def importance_form(self, feature_order, feature_name, feature_type, feature_importance):
        """
        변수 중요도를 반환하기 위한 형식
        
        매개변수
        feature_order : 변수 순서
        feature_name : 변수 이름
        feature_type : 변수 타입
        feature_importance : 변수 중요도
        """
        return {
            "featureOrder": feature_order,
            "featureName": feature_name,
            "type": feature_type,
            "importance": feature_importance
        }