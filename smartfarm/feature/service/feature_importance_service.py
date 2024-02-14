from ..serializers import GetFeatureImportanceSerializer
from ...models import FileFeature
from ...data_analytics.utils.rf_classifier import CustomRandomForestClassifier
from ...file.utils.utils import search_file_absolute_path
from ...file_data.service.get_file_data_service import GetFileDataService
from ...data_analytics.utils.linear import CustomLinearRegression

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

    def execute(self):
        model = CustomLinearRegression()
        print(self.file_object.id, self.x_value)
        queryset = FileFeature.objects.filter(file=self.file_object.id)
        file_absolute_path = search_file_absolute_path(self.file_object.file_root)
        df = GetFileDataService.file_to_df(file_absolute_path)
        model.fit(df[self.x_value], df[self.y_value])
        importances = model.feature_importances()
        for idx, name in enumerate(self.x_value):
            print(queryset, name)
            feature_obj = queryset.get(feature_name=name)
            feature_obj.feature_importance = importances[idx]
            feature_obj.save()

        return queryset.order_by('-feature_importance')