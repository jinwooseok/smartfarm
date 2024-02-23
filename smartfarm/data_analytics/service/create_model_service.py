from ...models import LearnedModel
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from ...file_data.service.get_file_data_service import GetFileDataService
from ...file_data.service.get_temp_data_service import GetTempDataService
from ...file.utils.utils import search_file_absolute_path
from .save_model_service import SaveModelService
from ..utils.rf_classifier import CustomRandomForestClassifier
from ..utils.linear import CustomLinearRegression
import pandas as pd

class CreateModelService():
    def __init__(self, model_name, x_value, y_value, model, file_object, file_data, train_size=0.7, is_save=False):
        self.model_name = model_name
        self.x_value = x_value
        self.y_value = y_value
        self.train_size = train_size
        self.model = model
        self.file_object = file_object
        self.file_data = file_data
        self.is_save = is_save
    
    @classmethod
    def from_serializer(cls, serializer, user) -> "CreateModelService":
        return cls(serializer.validated_data['modelName']
                    ,serializer.validated_data['xValue']
                    ,serializer.validated_data['yValue']
                    ,serializer.validated_data['model']
                    ,serializer.get_file_object(user)
                    ,serializer.validated_data['fileData']
                    ,serializer.validated_data['trainSize'])

    def execute(self):
        # file_absolute_path = search_file_absolute_path(instance.file_root)
        # df = GetFileDataService.file_to_df(file_absolute_path)
        json_data = self.file_data
        df = pd.DataFrame(json_data)
        df = df.dropna(axis=0)
        x_df = df[self.x_value]
        y_df = df[self.y_value]
        #모델 train_set 설정
        random_state = 42
        X_train, X_test, y_train, y_test = train_test_split(x_df, y_df, test_size=self.train_size, random_state=random_state)
        # 모델 생성 및 학습
        model = self.model_handler(X_train, y_train, random_state)
        result = model.predict(X_test, y_test)
        print(result)
        if self.is_save is True:
            if LearnedModel.objects.filter(user=self.file_object.user, original_file_name = self.file_object.file_title).exists():
                LearnedModel.objects.filter(user=self.file_object.user, original_file_name = self.file_object.file_title).delete()
            model_object = SaveModelService(self.file_object, model.learned_model, self.model_name, model.meta()).execute()
            result['model_name'] = model_object.model_name
        else:
            result['model_name'] = self.model_name
        return result
    
    def model_handler(self, x_train, y_train, random_state=42):
        if self.model == "random":
            model = CustomRandomForestClassifier(x_train, y_train, random_state)
            model.fit()
            return model 
        elif self.model == "linear":
            model = CustomLinearRegression(x_train, y_train, random_state)
            model.fit()
            return model