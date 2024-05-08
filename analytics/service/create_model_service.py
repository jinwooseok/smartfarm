"""
모델을 생성하는 서비스를 정의한 파일
"""
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from common.exceptions import (InvalidFeatureException, DataCountException, ModelTypeException)
from common.validators import serializer_validator
from analytics.serializers import (RFClassifierSerializer, RFRegressorSerializer,
                                   RidgeSerializer, LassoSerializer,
                                   ElasticSerializer, SVMSerializer,
                                   GBRegressorSerializer)
from analytics.service.save_model_service import SaveModelService
from analytics.utils.gradient_boosting import CustomGradientBoosting
from analytics.utils.linear import CustomLinearRegression
from analytics.utils.lasso import CustomLassoRegression
from analytics.utils.logistic import CustomLogisticRegression
from analytics.utils.rf_model import (CustomRandomForestClassifier, CustomRandomForestRegressor)
from analytics.utils.ridge import CustomRidgeRegression
from analytics.utils.elasticnet import CustomElasticNet
from analytics.utils.svm import (CustomSVC, CustomSVR)

class CreateModelService():
    """
    설명
    - 모델 생성 서비스 클래스. 모든 모델 생성 서비스를 분기하는 클래스이다.
    
    메서드
    - __init__: 모델 생성 서비스 객체 초기화 메소드
    - from_serializer: serializer로부터 CreateModelService 객체를 생성하는 메소드
    - execute: 모델 생성 서비스를 실행하는 메소드
    - model_handler: 모델 생성 서비스에서 사용하는 모델 핸들러 메소드
    """
    def __init__(self, model_name, x_value, y_value,
                 model, file_object, file_data,
                 model_params, train_size=0.7):
        """
        매개변수
        - model_name: 모델 파일명
        - x_value: 독립변수
        - y_value: 종속변수
        - model: 생성할 모델의 종류
        - file_object: 파일 객체
        - file_data: 파일 데이터
        - model_params: 모델 하이퍼파라미터
        - train_size: 학습 데이터 비율
        """
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
        """
        설명
        - serializer로부터 CreateModelService 객체를 생성하는 메서드
        
        매개변수
        - serializer: CreateModelSerializer 객체
        """
        return cls(serializer.validated_data['modelName']
                    ,serializer.validated_data['xValue']
                    ,serializer.validated_data['yValue']
                    ,serializer.validated_data['model']
                    ,serializer.get_file_object(user)
                    ,serializer.validated_data['fileData']
                    ,serializer.validated_data['modelParams']
                    ,serializer.validated_data['trainSize'])

    def execute(self):
        """
        설명
        - 모델 생성 서비스를 실행하는 메소드. 서드파티 모델을 통해 모델을 학습하고 결과 반환과 저장 과정을 수행한다.
        
        반환값
        - 형태 : dict
        
            {
                'model' : 설정한 모델 파일명 (str),
                'featureNames': 사용한 독립변수명 (list),
                'targetNames': 사용한 종속변수명 (str),
                'randomState': random seed 번호 (int),
                'MSE': Mean Squared Error를 소수점 4자리까지 반올림하여 표시 (float),
                'R2': R2 Score를 소수점 4자리까지 반올림하여 표시 (float),
                'testData': 테스트 데이터의 예측값, 실제값, 독립변수를 딕셔너리 형태로 반환 (list<dict>),
                'yPred': 예측값 리스트 (list),
                'y': 실제값 리스트 (list),
            }
        
        예외처리
        - InvalidFeatureException : x_value나 y_value가 데이터에 없을 경우 발생
        - DataCountException : 관측치가 독립변수 개수 + 1 보다 적을 경우 발생
        """
        # 1. 파일시스템에서 파일 데이터를 호출
        json_data = self.file_data
        df = pd.DataFrame(json_data)

        # 2. 선택한 독립변수와 종속변수가 데이터에 있는지 확인
        for name in self.x_value+[self.y_value]:
            if name not in df.columns:
                raise InvalidFeatureException(name)

        # 3. NaN이 포함된 행을 제거해 모델 생성 시 에러 발생 방지
        df.replace('', np.nan, inplace=True)
        df.dropna(axis=0, subset=self.x_value+[self.y_value], inplace=True)

        # 4. 데이터가 충분한지 확인 (독립변수 개수 + 1) 보다 적을 시 에러 발생
        if len(df) < len(self.x_value) + 1:
            raise DataCountException(len(self.x_value), len(df))

        # 5. x, y 데이터 분할
        x_df = df[self.x_value]
        y_df = df[self.y_value]
        random_state = 42
        x_train, x_test, y_train, y_test = train_test_split(x_df, y_df,
                                                            test_size=self.train_size,
                                                            random_state=random_state)

        # 6. 모델 생성 함수인 model_handler를 사용해 모델을 설정하고 학습을 진행
        model = self.model_handler(x_train, y_train, random_state)
        result = model.predict(x_test, y_test)

        # 7. 모델 저장 서비스 호출
        model_object = SaveModelService(self.file_object,
                                        model.learned_model,
                                        self.model_name,
                                        model.meta()
                                        ).execute()

        # 8. 결과 반환
        result['modelFileName'] = model_object.model_name
        return result

    def model_handler(self, x_train, y_train, random_state=42):
        """
        설명
        - 모델 생성 서비스에서 사용하는 모델 핸들러 메소드. 모델 종류에 따라 분기하여 모델을 생성한다.
        - 범주형 모델인 경우 encoding 진행 후 모델링
        - 이산형 모델인 경우 모델링
        
        매개변수
        - x_train: 학습 데이터의 독립변수
        - y_train: 학습 데이터의 종속변수
        - random_state: random seed 번호

        반환값
        - 형태 : 학습된 Model 객체
        
        예외처리
        - ModelTypeException: 지원하지 않는 모델이거나 맞지 않는 데이터 타입인 경우 발생
        """

        #회귀 모델
        if self.model == "rfr": # 랜덤포레스트 회귀
            nominal_columns = x_train.select_dtypes(include=['object', 'category']).columns
            if len(nominal_columns) > 0:
                raise ModelTypeException(nominal_columns, "명목형 혹은 범주형")
            if y_train.dtypes == "object":
                raise ModelTypeException(y_train.name, "명목형 혹은 범주형")
            serializer = RFRegressorSerializer(data = self.model_params)
            serializer = serializer_validator(serializer)
            model = CustomRandomForestRegressor(x_train, y_train,
                                                random_state,
                                                serializer.validated_data)
            model.fit()
            return model

        elif self.model == "linear": # 선형 회귀
            nominal_columns = x_train.select_dtypes(include=['object', 'category']).columns
            if len(nominal_columns) > 0:
                raise ModelTypeException(nominal_columns, "명목형 혹은 범주형")
            if y_train.dtypes == "object":
                raise ModelTypeException(y_train.name, "명목형 혹은 범주형")
            model = CustomLinearRegression(x_train, y_train,
                                           random_state, self.model_params)
            model.fit()
            return model

        elif self.model == "lasso": # 라쏘 회귀
            nominal_columns = x_train.select_dtypes(include=['object', 'category']).columns
            if len(nominal_columns) > 0:
                raise ModelTypeException(nominal_columns, "명목형 혹은 범주형")
            if y_train.dtypes == "object":
                raise ModelTypeException(y_train.name, "명목형 혹은 범주형")
            serializer = LassoSerializer(data = self.model_params)
            serializer = serializer_validator(serializer)
            model = CustomLassoRegression(x_train, y_train,
                                          random_state, serializer.validated_data)
            model.fit()
            return model

        elif self.model == "ridge": # 릿지 회귀
            nominal_columns = x_train.select_dtypes(include=['object', 'category']).columns
            if len(nominal_columns) > 0:
                raise ModelTypeException(nominal_columns, "명목형 혹은 범주형")
            if y_train.dtypes == "object":
                raise ModelTypeException(y_train.name, "명목형 혹은 범주형")
            serializer = RidgeSerializer(data = self.model_params)
            serializer = serializer_validator(serializer)
            model = CustomRidgeRegression(x_train, y_train,
                                          random_state, serializer.validated_data)
            model.fit()
            return model

        elif self.model == "logistic": # 로지스틱 회귀
            model = CustomLogisticRegression(x_train, y_train,
                                             random_state, self.model_params)
            model.fit()
            return model

        elif self.model == "svr": # 서포트 벡터 머신 회귀
            if y_train.dtypes == "object":
                raise ModelTypeException(y_train.name, "명목형 혹은 범주형")
            serializer = SVMSerializer(data = self.model_params)
            serializer = serializer_validator(serializer)
            model = CustomSVR(x_train, y_train,
                              random_state, serializer.validated_data)
            model.fit()
            return model

        elif self.model == "gb": # 그래디언트 부스팅 회귀
            nominal_columns = x_train.select_dtypes(include=['object', 'category']).columns
            if len(nominal_columns) > 0:
                raise ModelTypeException(nominal_columns, "명목형 혹은 범주형")
            if y_train.dtypes == "object":
                raise ModelTypeException(y_train.name, "명목형 혹은 범주형")
            serializer = GBRegressorSerializer(data = self.model_params)
            serializer = serializer_validator(serializer)
            model = CustomGradientBoosting(x_train, y_train,
                                           random_state, serializer.validated_data)
            model.fit()
            return model

        elif self.model == "elastic": # 엘라스틱넷 회귀
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

        #분류 모델
        elif self.model == "rf": # 랜덤포레스트 분류
                serializer = RFClassifierSerializer(data = self.model_params)
                serializer = serializer_validator(serializer)
                model = CustomRandomForestClassifier(x_train, y_train,
                                                     random_state, serializer.validated_data)
                model.fit()
                return model 

        elif self.model == "svc": # 서포트 벡터 머신 분류
            serializer = SVMSerializer(data = self.model_params)
            serializer = serializer_validator(serializer)
            model = CustomSVC(x_train, y_train,
                              random_state, serializer.validated_data)
            model.fit()
            return model
        
        #미지원 모델
        elif self.model == "knn": # K-최근접 이웃
            raise ModelTypeException("KNN", "KNN은 아직 지원하지 않습니다.")
        elif self.model == "dt": # 의사결정나무
            raise ModelTypeException("Decision Tree", "Decision Tree는 아직 지원하지 않습니다.")
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