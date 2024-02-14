from django.shortcuts import render
import pandas as pd
#분석도구들을 모아놓은 파일
import statsmodels.api as sm  

class CustomLinearRegression:
    def __init__(self):
        self.model = sm.OLS
        self.learned_model = None
        
    def fit(self, x_dataset, y_dataset):
        self.learned_model = self.model(endog=x_dataset, exog=y_dataset).fit()
        return self.learned_model
    
    def feature_importances(self):
        return self.learned_model.params