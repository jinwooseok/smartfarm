from ...data_analytics.utils.rf_classifier import CustomRandomForestClassifier
from ...file.utils.utils import *
from ...file_data.service.get_file_data_service import GetFileDataService
class FeatureService:
    @staticmethod
    def extract_feature(instance):
        file_absolute_path = search_file_absolute_path(instance.file_root)
        data = GetFileDataService.file_to_df(file_absolute_path)
        feature_info_list = []
        for idx, column in enumerate(data.columns):
            column_info = {
                "file":instance.id,
                "feature_order": idx,
                "feature_name": column,
                "feature_type": str(data[column].dtype),
                "feature_importance": None,
                "feature_selected" : False,
            }
            print(column_info)
            feature_info_list.append(column_info)
        return feature_info_list
    
