from sklearn.linear_model import LogisticRegression
from analytics.utils.linear import CustomLinearRegression
from analytics.utils.encoder import Encoder
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score

class CustomLogisticRegression(CustomLinearRegression):
    def __init__(self, x_train, y_train, sample_random_state, model_params):
        self.model = LogisticRegression()
        self.learned_model = None
        self.x_train = Encoder.encode(x_train, method = 'label')
        self.y_train = Encoder.encode(y_train, method = 'label')
        self.sample_random_state = sample_random_state
        self.model_params = model_params
        self.model_name = 'Logistic Regression'
    
    def fit(self):
        self.learned_model = self.model.fit(self.x_train, self.y_train)
        return self.learned_model
    
    def predict(self, x_test, y_test):
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
        return {
            'model': self.model_name,
            'featureNames': list(self.x_train.columns),
            'targetNames': self.y_train.name,
            'randomState': self.sample_random_state,
        }