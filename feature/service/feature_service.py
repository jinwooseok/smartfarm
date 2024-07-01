"""
파일의 feature를 추출하는 service
"""
import json
from file.utils.utils import *
from file_data.service.get_file_data_service import GetFileDataService

class FeatureService:
    """
    파일의 feature를 추출하는 서비스
    
    메서드
    extract_feature : 파일의 feature를 추출하여 반환
    extract_model_feature : 모델의 feature를 추출하여 반환
    
    """
    @staticmethod
    def extract_feature(instance):
        """
        파일의 feature를 추출하여 반환
        
        매개변수
        instance : 파일 인스턴스
        
        기능
        1. 파일의 절대 경로를 찾음
        2. 파일을 DataFrame으로 변환
        3. feature_info_list에 feature 정보를 추가
        4. feature_info_list 반환
        """
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
            feature_info_list.append(column_info)
        return feature_info_list
    
    @staticmethod
    def extract_model_feature(instance):
        """
        모델의 feature를 추출하여 반환
        
        매개변수
        instance : 모델 인스턴스
        
        기능
        1. 모델 메타 파일의 절대 경로를 찾음
        2. 모델 메타 파일을 읽음
        3. feature_info_list에 feature 정보를 추가
        4. feature_info_list 반환
        """
        file_absolute_path = search_file_absolute_path(instance.model_meta_root)
        with open (file_absolute_path, "r") as f:
            model_meta = json.load(f)
            
        feature_info_list = []
        #x변수 추출
        for idx, column in enumerate(model_meta['feature_names']):
            column_info = {
                "model":instance.id,
                "feature_name": column,
                "feature_type": "feature",
                "weight": model_meta['model_weights'][idx],
            }
            feature_info_list.append(column_info)
        #y변수 추출
        column_info = {
            "model":instance.id,
            "feature_name": model_meta['target_names'],
            "feature_type": "target",
            "weight": None,
        }
        feature_info_list.append(column_info)
        return feature_info_list
