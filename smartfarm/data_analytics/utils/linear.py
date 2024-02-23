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
        y_pred.name = y_test.name + '_pred'
        # 예측 결과 평가
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        # 추가적인 예측 결과 리턴
        return {
            'model' : 'Linear Regression',
            'featureNames': list(self.x_dataset.columns),
            'targetNames': self.y_dataset.name,
            'randomState': self.random_state,
            'MSE': mse,
            'R2': r2,
            'testData': pd.concat([x_test, y_test, y_pred], axis=1).to_dict(orient='records'),
            'yPred': y_pred.tolist(),
            'y': y_test.tolist()
        }