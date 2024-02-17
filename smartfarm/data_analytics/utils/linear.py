from django.shortcuts import render
import pandas as pd
#분석도구들을 모아놓은 파일
import statsmodels.api as sm  
from sklearn.metrics import mean_squared_error, r2_score
class CustomLinearRegression:
    def __init__(self, x_dataset, y_dataset, random_state):
        self.model = sm.OLS
        self.learned_model = None
        self.x_dataset = x_dataset
        self.y_dataset = y_dataset
        self.random_state = random_state
        
    def fit(self):
        self.learned_model = self.model(endog=self.y_dataset, exog=self.x_dataset).fit()
        return self.learned_model
    
    def feature_importances(self):
        return self.learned_model.params
    
    def meta(self):
        return {
                'model' : 'Linear Regression',
                'feature_names': list(self.x_dataset.columns),
                'target_names': self.y_dataset.name,
                'model_weights': self.learned_model.params.values.tolist(),
                'random_state': self.random_state
            }
    
    def predict(self, x_test, y_test):
        y_pred = self.learned_model.predict(x_test)
        # 예측 결과 평가
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        # 추가적인 예측 결과 리턴
        return {
            'model' : 'Linear Regression',
            'feature_names': list(self.x_dataset.columns),
            'target_names': self.y_dataset.name,
            'model_weights': self.learned_model.params.values.tolist(),
            'random_state': self.random_state,
            'mean_squared_error': mse,
            'r2_score': r2
        }