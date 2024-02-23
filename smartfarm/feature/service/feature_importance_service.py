from ..serializers import GetFeatureImportanceSerializer
import pandas as pd
from ...data_analytics.utils.correlation import calculate_correlation
import numpy as np
class FeatureImportanceService:
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
        df = pd.DataFrame(self.data)
        response = []
        for idx, name in enumerate(self.x_value):
            feature_importance = calculate_correlation(df, name, self.y_value)
            if feature_importance is not None and np.isnan(feature_importance):
                feature_importance = None
            form = self.importance_form(idx, name, str(df[name].dtype), feature_importance)
            response.append(form)
        print(response)
        return response
    
    def importance_form(self, feature_order, feature_name, feature_type, feature_importance):
        return {
            "featureOrder": feature_order,
            "featureName": feature_name,
            "featureType": feature_type,
            "featureImportance": feature_importance
        }