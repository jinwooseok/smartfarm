import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from ...file_data.service.get_file_data_service import GetFileDataService
from ...file.utils.utils import search_file_absolute_path
from .save_model_service import SaveModelService
from ..utils.rf_classifier import CustomRandomForestClassifier

class CreateModelService():
    def __init__(self, model_name, x_value, y_value, train_size, model, file_object):
        self.model_name = model_name
        self.x_value = x_value
        self.y_value = y_value
        self.train_size = train_size
        self.model = model
        self.file_object = file_object
    
    @classmethod
    def from_serializer(cls, serializer, user) -> "CreateModelService":
        return cls(serializer.validated_data['modelName']
                   , serializer.validated_data['xValue']
                   , serializer.validated_data['yValue']
                   , serializer.validated_data['trainSize']
                   , serializer.validated_data['model']
                   , serializer.get_file_object(user))

    def execute(self):
        file_absolute_path = search_file_absolute_path(self.file_object.file_root)
        df = GetFileDataService.file_to_df(file_absolute_path)
        x_df = df[self.x_value]
        y_df = df[self.y_value]
        #모델 train_set 설정
        X_train, X_test, y_train, y_test = train_test_split(x_df, y_df, test_size=0.2, random_state=42)
        # 모델 생성 및 학습
        model = self.model_handler()
        model.fit(X_train, y_train)
        
        # 학습된 모델의 변수와 가중치 정보 추출
        model_meta = {
            'feature_names': x_df.columns,
            'target_names': y_df.unique(),
            'model_params': model.get_params(),
            'model_weights': model.feature_importances_
        }
        
        #모델 저장
        SaveModelService(model, self.model_name, model_meta).execute()
        
    def model_handler(self):
        if self.model == "random":
            model = CustomRandomForestClassifier()
            model.fit(self.x_value, self.y_value)
            return model.learned_model