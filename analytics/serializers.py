"""
직렬화 모듈들을 모아놓은 파일. 저장에 적합한 형태 혹은 전달에 적합한 형태로 데이터를 변환하는 역할을 한다.
"""
from rest_framework import serializers
from file.serializers import FileNameSerializer
from analytics.models import LearnedModel
from common.exceptions import *
from django.core.validators import MinValueValidator, MaxValueValidator
class CreateModelSerializer(FileNameSerializer):
    """
    모델 생성 시 사용되는 직렬화 클래스. api로 전달되는 데이터를 변환한다.
    - modelName (str): 모델 파일명
    - xValue (str): 독립변수
    - yValue (str): 종속변수
    - trainSize (float): 학습 데이터 비율
    - fileData (list): 파일 데이터
    - modelParams (dict): 모델 하이퍼파라미터
    - model (str): 모델 이름
    """
    modelName = serializers.CharField()
    xValue = serializers.JSONField()
    yValue = serializers.CharField()
    trainSize = serializers.FloatField()
    fileData = serializers.JSONField()
    modelParams = serializers.JSONField(required=False, default={})
    model = serializers.ChoiceField(choices=[("linear","linear")
                                             ,("logistic","logistic")
                                             ,("ridge","ridge")
                                             ,("lasso","lasso")
                                             ,("elastic","elastic")
                                             ,("decision","decision")
                                             ,("rf","rf")
                                             ,("rfr","rfr")
                                             ,("gb","gb")
                                             ,("ada","ada")
                                             ,("xgb","xgb")
                                             ,("lightgbm","lightgbm")
                                             ,("catboost","catboost")
                                             ,("svc","svc")
                                             ,("svr","svr")
                                             ,("elastic","elastic")
                                             ,("naive","naive")])

class RidgeSerializer(serializers.Serializer):
    """
    Ridge 모델 하이퍼파라미터 직렬화 클래스
    - random_state (int): 랜덤 시드
    - alpha (float): alpha 값
    """
    random_state = serializers.IntegerField(default=42, required=False)
    alpha = serializers.FloatField(default=1.0, required=False, validators=[MinValueValidator(0)])

class LassoSerializer(serializers.Serializer):
    """
    Lasso 모델 하이퍼파라미터 직렬화 클래스
    - random_state (int): 랜덤 시드
    - alpha (float): alpha 값
    """
    random_state = serializers.IntegerField(default=42, required=False)
    alpha = serializers.FloatField(default=1.0, required=False, validators=[MinValueValidator(0)])

class ElasticSerializer(serializers.Serializer):
    """
    Elastic 모델 하이퍼파라미터 직렬화 클래스
    - random_state (int): 랜덤 시드
    - alpha (float): alpha 값
    - l1_ratio (float): l1_ratio 값
    """
    random_state = serializers.IntegerField(default=42, required=False)
    alpha = serializers.FloatField(default=1.0, required=False,
                                   validators=[MinValueValidator(0)])
    l1_ratio = serializers.FloatField(default=0.5, required=False,
                                      validators=[MinValueValidator(0), MaxValueValidator(1)])

class SVMSerializer(serializers.Serializer):
    """
    SVM 모델 하이퍼파라미터 직렬화 클래스
    - kernel (str): 커널 종류
    """
    kernel = serializers.ChoiceField(choices=["linear", "poly", "rbf", "sigmoid"],
                                     default="rbf", required=False)

class RFRegressorSerializer(serializers.Serializer):
    """
    RandomForestRegressor 모델 하이퍼파라미터 직렬화 클래스
    - n_estimators (int): 트리 개수
    - max_depth (int): 최대 깊이
    """
    n_estimators = serializers.IntegerField(default=100, required=False,
                                            validators=[MinValueValidator(1)])
    max_depth = serializers.IntegerField(default=3, required=False,
                                         validators=[MinValueValidator(1)])

class GBRegressorSerializer(serializers.Serializer):
    """
    GradientBoostingRegressor 모델 하이퍼파라미터 직렬화 클래스
    - n_estimators (int): 트리 개수
    - learning_rate (float): 학습률
    - max_depth (int): 최대 깊이
    """
    n_estimators = serializers.IntegerField(default=100, required=False, 
                                            validators=[MinValueValidator(1)])
    learning_rate = serializers.FloatField(default=0.1, required=False,
                                           validators=[MinValueValidator(0)])
    max_depth = serializers.IntegerField(default=3, required=False,
                                         validators=[MinValueValidator(1)])

class RFClassifierSerializer(serializers.Serializer):
    """
    RandomForestClassifier 모델 하이퍼파라미터 직렬화 클래스
    - n_estimators (int): 트리 개수
    - max_depth (int): 최대 깊이
    """
    n_estimators = serializers.IntegerField(default=100, required=False,
                                            validators=[MinValueValidator(1)])
    max_depth = serializers.IntegerField(default=3, required=False,
                                         validators=[MinValueValidator(1)])

class ModelNameSerializer(serializers.Serializer):
    """
    모델 이름 직렬화 클래스
    - modelName (str): 모델 이름
    """
    modelName = serializers.CharField()

    def get_model_object(self, user)->LearnedModel:
        """
        try : 모델 객체 반환
        except : 파일 없음 예외 발생
        """
        try:
            return LearnedModel.objects.get(user=user, model_name=self.data['modelName'])
        except LearnedModel.DoesNotExist:
            raise FileNotFoundException()

class PredictModelSerializer(ModelNameSerializer):
    """
    모델 예측 시 사용되는 직렬화 클래스. api로 전달되는 데이터를 변환한다.
    - testData (list): 테스트 데이터
    - xValue (str): 독립변수
    - yValue (str): 종속변수
    """
    testData = serializers.JSONField()
    xValue = serializers.CharField()
    yValue = serializers.CharField()
