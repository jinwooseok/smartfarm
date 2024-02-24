from ...models import LearnedModel
from sklearn.model_selection import train_test_split
from .save_model_service import SaveModelService
from ..utils.rf_model import CustomRandomForestClassifier, CustomRandomForestRegressor
from ..utils.linear import CustomLinearRegression
from ..utils.lasso import CustomLassoRegression
from ..utils.ridge import CustomRidgeRegression
from ..utils.logistic import CustomLogisticRegression
from ..utils.svm import CustomSVC, CustomSVR
from ..utils.gradient_boosting import CustomGradientBoosting
from ..utils.elasticnet import CustomElasticNet
from ..serializers import *
from common.validators import serializer_validator
import pandas as pd
from ..exceptions.model_type_exception import ModelTypeException
from ..exceptions.data_count_exception import DataCountException
import numpy as np
from ..utils.encoder import Encoder
class CreateModelService():
    def __init__(self, model_name, x_value, y_value, model, file_object, file_data, train_size=0.7, model_params={}):
        self.model_name = model_name
        self.x_value = x_value
        self.y_value = y_value
        self.train_size = train_size
        self.model = model
        self.file_object = file_object
        self.file_data = file_data
        self.model_params = model_params
    
    @classmethod
    def from_serializer(cls, serializer, user) -> "CreateModelService":
        return cls(serializer.validated_data['modelName']
                    ,serializer.validated_data['xValue']
                    ,serializer.validated_data['yValue']
                    ,serializer.validated_data['model']
                    ,serializer.get_file_object(user)
                    ,serializer.validated_data['fileData']
                    ,serializer.validated_data['trainSize']
                    ,serializer.validated_data['modelParams'])

    def execute(self):
        # file_absolute_path = search_file_absolute_path(instance.file_root)
        # df = GetFileDataService.file_to_df(file_absolute_path)
        json_data = self.file_data
        df = pd.DataFrame(json_data)
        df.replace('', np.nan, inplace=True)
        df.dropna(axis=0, subset=self.x_value+[self.y_value], inplace=True) #nan 제거
        if len(df) < len(self.x_value) + 1:
            raise DataCountException(len(self.x_value), len(df))
        
        x_df = df[self.x_value]
        y_df = df[self.y_value]
        #모델 train_set 설정
        random_state = 42
        X_train, X_test, y_train, y_test = train_test_split(x_df, y_df, test_size=self.train_size, random_state=random_state)
        # 모델 생성 및 학습
        model = self.model_handler(X_train, y_train, random_state)
        result = model.predict(X_test, y_test)
        # if self.is_save is True:
        model_object = SaveModelService(self.file_object, model.learned_model, self.model_name, model.meta()).execute()
        result['modelFileName'] = model_object.model_name
        return result
    
    def model_handler(self, x_train, y_train, random_state=42):
        if self.model == "rf":
            serializer = RFClassifierSerializer(data = self.model_params)
            serializer = serializer_validator(serializer)
            
            model = CustomRandomForestClassifier(x_train, y_train, random_state, serializer.validated_data)
            model.fit()
            return model 
        
        elif self.model == "rfr":
            nominal_columns = x_train.select_dtypes(include=['object', 'category']).columns
            if len(nominal_columns) > 0:
                raise ModelTypeException(nominal_columns, "명목형 혹은 범주형")
            if y_train.dtypes == "object":
                raise ModelTypeException(y_train.name, "명목형 혹은 범주형")
            serializer = RFRegressorSerializer(data = self.model_params)
            serializer = serializer_validator(serializer)
            model = CustomRandomForestRegressor(x_train, y_train, random_state, serializer.validated_data)
            model.fit()
            return model
        
        elif self.model == "linear":
            nominal_columns = x_train.select_dtypes(include=['object', 'category']).columns
            if len(nominal_columns) > 0:
                raise ModelTypeException(nominal_columns, "명목형 혹은 범주형")
            if y_train.dtypes == "object":
                raise ModelTypeException(y_train.name, "명목형 혹은 범주형")
            model = CustomLinearRegression(x_train, y_train, random_state, self.model_params)
            model.fit()
            return model
        
        elif self.model == "lasso":
            nominal_columns = x_train.select_dtypes(include=['object', 'category']).columns
            if len(nominal_columns) > 0:
                raise ModelTypeException(nominal_columns, "명목형 혹은 범주형")
            if y_train.dtypes == "object":
                raise ModelTypeException(y_train.name, "명목형 혹은 범주형")
            serializer = LassoSerializer(data = self.model_params)
            serializer = serializer_validator(serializer)
            model = CustomLassoRegression(x_train, y_train, random_state, serializer.validated_data)
            model.fit()
            return model
        
        elif self.model == "ridge":
            nominal_columns = x_train.select_dtypes(include=['object', 'category']).columns
            if len(nominal_columns) > 0:
                raise ModelTypeException(nominal_columns, "명목형 혹은 범주형")
            if y_train.dtypes == "object":
                raise ModelTypeException(y_train.name, "명목형 혹은 범주형")
            serializer = RidgeSerializer(data = self.model_params)
            serializer = serializer_validator(serializer)
            model = CustomRidgeRegression(x_train, y_train, random_state, serializer.validated_data)
            model.fit()
            return model
        
        elif self.model == "logistic":
            if y_train.dtypes != "object":
                raise ModelTypeException(y_train.name, "연속형")
            model = CustomLogisticRegression(x_train, y_train, random_state, self.model_params)
            model.fit()
            return model
         
        elif self.model == "svc":
            if y_train.dtypes != "object":
                raise ModelTypeException(y_train.name, "연속형")
            serializer = SVMSerializer(data = self.model_params)
            serializer = serializer_validator(serializer)
            model = CustomSVC(x_train, y_train, random_state, serializer.validated_data)
            model.fit()
            return model
        
        elif self.model == "svr":
            if y_train.dtypes == "object":
                raise ModelTypeException(y_train.name, "명목형 혹은 범주형")
            serializer = SVMSerializer(data = self.model_params)
            serializer = serializer_validator(serializer)
            model = CustomSVR(x_train, y_train, random_state, serializer.validated_data)
            model.fit()
            return model
        
        elif self.model == "knn":
            raise ModelTypeException("KNN", "KNN은 아직 지원하지 않습니다.")
        elif self.model == "dt":
            raise ModelTypeException("Decision Tree", "Decision Tree는 아직 지원하지 않습니다.")
        
        elif self.model == "gb":
            nominal_columns = x_train.select_dtypes(include=['object', 'category']).columns
            if len(nominal_columns) > 0:
                raise ModelTypeException(nominal_columns, "명목형 혹은 범주형")
            if y_train.dtypes == "object":
                raise ModelTypeException(y_train.name, "명목형 혹은 범주형")
            
            serializer = GBRegressorSerializer(data = self.model_params)
            serializer = serializer_validator(serializer)
            model = CustomGradientBoosting(x_train, y_train, random_state, serializer.validated_data)
            model.fit()
            return model
        
        elif self.model == "elastic":
            nominal_columns = x_train.select_dtypes(include=['object', 'category']).columns
            if len(nominal_columns) > 0:
                raise ModelTypeException(nominal_columns, "명목형 혹은 범주형")
            if y_train.dtypes == "object":
                raise ModelTypeException(y_train.name, "명목형 혹은 범주형")
            serializer = ElasticSerializer(data = self.model_params)
            serializer = serializer_validator(serializer)
            model = CustomElasticNet(x_train, y_train, random_state, serializer.validated_data)
            model.fit()
            return model
        
        elif self.model == "xgb":
            raise ModelTypeException("XGBoost", "XGBoost는 아직 지원하지 않습니다.")
        elif self.model == "lgbm":
            raise ModelTypeException("LightGBM", "LightGBM은 아직 지원하지 않습니다.")
        elif self.model == "catboost":
            raise ModelTypeException("CatBoost", "CatBoost는 아직 지원하지 않습니다.")
        elif self.model == "ada":
            raise ModelTypeException("AdaBoost", "AdaBoost는 아직 지원하지 않습니다.")
        elif self.model == "naive":
            raise ModelTypeException("Naive Bayes", "Naive Bayes는 아직 지원하지 않습니다.")
        else:
            raise ModelTypeException(self.model, "지원하지 않는 모델입니다.")