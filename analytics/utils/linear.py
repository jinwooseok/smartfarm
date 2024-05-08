import numpy as np
import pandas as pd
#분석도구들을 모아놓은 파회귀 모델 종류일
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
class CustomLinearRegression:
    def __init__(self, x_train, y_train, sample_random_state, model_params):
        self.model = LinearRegression()
        self.learned_model = None
        self.x_train = x_train
        self.y_train = y_train
        self.sample_random_state = sample_random_state
        self.model_params = model_params
        self.model_name = 'Linear Regression'

    def fit(self):
        self.learned_model = self.model.fit(self.x_train, self.y_train)
        return self.learned_model

    def meta(self):
        return {
            'model': self.model_name,
            'featureNames': list(self.x_train.columns),
            'targetNames': self.y_train.name,
            'randomState': self.sample_random_state,
        }

    def predict(self, x_test, y_test):
        y_pred = self.learned_model.predict(x_test)
        y_pred = np.round(y_pred, decimals=4)
        x_test = x_test.reset_index(drop=True)
        y_test = y_test.reset_index(drop=True)
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