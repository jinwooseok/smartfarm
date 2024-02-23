from ..serializers import GetFeatureImportanceSerializer
from ...models import FileFeature
from ...data_analytics.utils.rf_classifier import CustomRandomForestClassifier
from ...file.utils.utils import search_file_absolute_path
from ...file_data.service.get_file_data_service import GetFileDataService
from ...data_analytics.utils.linear import CustomLinearRegression
from ...data_analytics.utils.correlation import calculate_correlation
class FeatureImportanceService:
    def __init__(self, x_value, y_value, data=None):
        self.x_value = x_value
        self.y_value = y_value
        self.data = data
    
    @classmethod
    def from_serializer(cls, serializer: GetFeatureImportanceSerializer, user):
        return cls(serializer.validated_data['xValue']
                   ,serializer.validated_data['yValue']
                   ,serializer.validated_data['data'])

    def execute(self):
        df = self.data
        response = []
        for idx, name in enumerate(self.x_value):
            feature_importance = calculate_correlation(df, name, self.y_value)
            form = self.importance_form(idx, name, str(df[name].dtype), feature_importance)
            response.append(form)
        return response
    
    def importance_form(self, feature_order, feature_name, feature_type, feature_importance):
        return {
            "featureOrder": feature_order,
            "featureName": feature_name,
            "featureType": feature_type,
            "featureImportance": feature_importance
        }