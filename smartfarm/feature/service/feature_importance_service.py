from ..serializers import GetFeatureImportanceSerializer
from ...models import FileFeature
from ...data_analytics.utils.rf_classifier import CustomRandomForestClassifier

class FeatureImportanceService:
    def __init__(self, x_value, y_value, file_object):
        self.x_value = x_value
        self.y_value = y_value
        self.file_object = file_object
    
    @classmethod
    def from_serializer(cls, serializer: GetFeatureImportanceSerializer, user):
        return cls(serializer.validated_data['xValue']
                   ,serializer.validated_data['yValue']
                   ,serializer.get_file_object(user))

    def get_feature_importance(self):
        queryset = FileFeature.objects.filter(file=self.file_object)
        model = CustomRandomForestClassifier().fit(self.x_value, self.y_value)
        importances = model.feature_importances()
        for feature_obj, importance in zip(queryset, importances):
                feature_obj.feature_importance = importance
                feature_obj.save()

        return queryset.order_by('-feature_importance')