from django.shortcuts import render
import pandas as pd
#분석도구들을 모아놓은 파일
import statsmodels.api as sm  

class CustomLinearRegression:
    def __init__(self, x_dataset, y_dataset):
        self.model = sm.OLS
        self.learned_model = None
        self.x_dataset = x_dataset
        self.y_dataset = y_dataset
        
    def fit(self):
        self.learned_model = self.model(endog=self.x_dataset, exog=self.y_dataset).fit()
        return self.learned_model
    
    def feature_importances(self):
        return self.learned_model.params
    
    def meta(self):
        return {
                'model_name' : 'Linear Regression',
                'feature_names': list(self.x_dataset.columns),
                'target_names': self.y_dataset.name,
                'model_weights': self.learned_model.params.values.tolist()
            }