"""
저장된 모델을 불러와서 예측을 수행하는 서비스를 제공하는 파일 (미완성)
"""
import pickle
from analytics.utils.linear import CustomLinearRegression

class PredictModelService:
    """
    설명
    - 저장된 모델을 불러와서 예측을 수행하는 서비스 (미완성)
    
    메서드
    - __init__: 초기화 메서드
    - from_serializer: 직렬화된 데이터를 받아서 객체를 생성하는 메서드
    - execute: 예측 서비스을 실행하는 메서드
    - model_handler: 모델에 따라 예측을 수행하는 메서드
    - load_model: 모델을 불러오는 메서드
    """
    def __init__(self, model_object, test_data, x_value, y_value):
        """
        매개변수
        - model_object (LearnedModel): 모델 객체
        - test_data (DataFrame): 새로 예측하고자 하는 데이터
        - x_value (str): 독립변수
        - y_value (str): 종속변수
        """
        self.model_object = model_object
        self.test_data = test_data
        self.x_value = x_value
        self.y_value = y_value
        self.loaded_model = None

    @classmethod
    def from_serializer(cls, serializer, user) -> "PredictModelService":
        """
        설명
        - serializer로부터 PredictModelService 객체를 생성하는 메서드
        
        매개변수
        - serializer : PredictModelSerializer 객체
        """
        return cls(serializer.get_model_object(user)
                   ,serializer.validated_data['testData']
                   ,serializer.validated_data['xValue']
                   ,serializer.validated_data['yValue'])

    def execute(self):
        """
        설명
        - 예측 서비스를 실행하는 메서드. 요청한 모델에 따라 새로 분석 수행
        - CreateModelService의 execute와 동일하지만 저장된 모델을 사용한다는 차이가 있음
        
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
        """
        x_test = self.test_data[self.x_value]
        y_test = self.test_data[self.y_value]
        self.loaded_model = self.load_model()
        result = self.model_handler(x_test, y_test)
        return result

    def model_handler(self, x_df, y_df, random_state=42):
        """
        설명
        - linear만 테스트
        """
        if self.model_object.model == "linear":
            model = CustomLinearRegression(x_df, y_df, random_state, model_params=dict())
            model.learned_model = self.loaded_model
            result = model.predict(x_df, y_df)
            return result

    def load_model(self):
        """
        설명
        - 저장된 모델을 불러오는 메서드
        
        반환값
        - 불러온 모델 객체
        """
        model = pickle.load(self.model_object)
        return model
