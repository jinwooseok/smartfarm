from ...data_analytics.utils.rf_classifier import CustomRandomForestClassifier
class FeatureService:
    @staticmethod
    def extract_feature(file_id,data):
        feature_info_list = []
        for idx, column in enumerate(data.columns):
            column_info = {
                "file":file_id,
                "feature_order": idx,
                "feature_name": column,
                "feature_type": str(data[column].dtype),
                "feature_importance": None,
                "feature_selected" : False,
            }
            feature_info_list.append(column_info)
        return feature_info_list
    
