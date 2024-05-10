"""
로지스틱 회귀분석 클래스
"""
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LogisticRegression
from analytics.utils.linear import CustomLinearRegression
from analytics.utils.encoder import Encoder

class CustomLogisticRegression(CustomLinearRegression):
    """
    설명
    - 로지스틱 회귀분석을 수행하는 클래스
    - 범주형 데이터를 처리하기 위해 Encoder 클래스를 사용하여 데이터를 변환
    
    메서드
    - fit(): 모델을 학습
    - predict(): 모델을 사용하여 예측
    - meta(): 모델의 메타 정보를 리턴
    """
    def __init__(self, x_train, y_train, sample_random_state, model_params):
        """
        매개변수
        - x_train (pd.DataFrame): 훈련 데이터의 독립변수
        - y_train (pd.Series): 훈련 데이터의 종속변수
        - sample_random_state (int): 훈련 데이터 분할 시 사용할 시드값
        - model_params (dict): 모델 초기화 시 사용할 매개변수
        """
        super().__init__(x_train, y_train, sample_random_state, model_params)
        self.model = LogisticRegression()
        self.learned_model = None
        self.x_train = Encoder.encode(x_train, method = 'label')
        self.y_train = Encoder.encode(y_train, method = 'label')
        self.sample_random_state = sample_random_state
        self.model_params = model_params
        self.model_name = 'Logistic Regression'
    
    def fit(self):
        """
        설명
        - 모델을 학습
        
        반환값
        - 학습된 모델 객체
        """
        self.learned_model = self.model.fit(self.x_train, self.y_train)
        return self.learned_model
    
    def predict(self, x_test, y_test):
        """
        설명
        - 모델 객체를 사용하여 예측을 수행
        
        매개변수
        - x_test (pd.DataFrame): 테스트 데이터의 독립변수
        - y_test (pd.Series): 테스트 데이터의 종속변수
        
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
        x_test = Encoder.encode(x_test, method = 'label').reset_index(drop=True)
        y_test = Encoder.encode(y_test, method = 'label').reset_index(drop=True)
        y_pred = self.learned_model.predict(x_test)
        y_pred = np.round(y_pred, decimals=4)
        y_pred = pd.Series(y_pred, name=y_test.name + '_pred').reset_index(drop=True)
        
        # 예측 결과 평가
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        # 추가적인 예측 결과 리턴
        return {
            'model' : self.model_name,
            'featureNames': list(self.x_train.columns),
            'targetNames': self.y_train.name,
            'randomState': self.sample_random_state,
            'MSE': round(mse, 4),
            'R2': round(r2, 4),
            'testData': pd.concat([x_test, y_test, y_pred], axis=1).to_dict(orient='records'),
            'yPred': y_pred.tolist(),
            'y': y_test.tolist()
        }

    def meta(self):
        """
        설명
        - 모델의 메타 정보 폼을 생성하고 반환. 모델 정보를 저장하기 위한 용도로 사용됨
        
        반환값
        - 모델의 메타 정보를 담은 딕셔너리
        """
        return {
            'model': self.model_name,
            'featureNames': list(self.x_train.columns),
            'targetNames': self.y_train.name,
            'randomState': self.sample_random_state,
        }