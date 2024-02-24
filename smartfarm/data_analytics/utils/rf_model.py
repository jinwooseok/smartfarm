from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score

class CustomRandomForestClassifier():
    def __init__(self, x_dataset, y_dataset, sample_random_state, model_params):
        self.model = RandomForestClassifier(**model_params)
        self.learned_model = None
        self.x_dataset = x_dataset
        self.y_dataset = y_dataset
        self.sample_random_state = sample_random_state
        self.model_params = model_params
        self.model_name = 'Random Forest Classifier'
    
    def fit(self):
        self.learned_model = self.model.fit(self.x_dataset, self.y_dataset)
        return self.learned_model
    
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
            'featureNames': list(self.x_dataset.columns),
            'targetNames': self.y_dataset.name,
            'randomState': self.sample_random_state,
            'MSE': round(mse, 4),
            'R2': round(r2, 4),
            'testData': pd.concat([x_test, y_test, y_pred], axis=1).to_dict(orient='records'),
            'yPred': y_pred.tolist(),
            'y': y_test.tolist()
        }
    def feature_importances(self):
        return self.learned_model.feature_importances_
    
    def meta(self):
        return {
                'model_name' : self.model_name,
                'feature_names': list(self.x_dataset.columns),
                'target_names': self.y_dataset.name,
                'model_weights': list(self.learned_model.feature_importances_),
                'random_state': self.sample_random_state
            }
    
class CustomRandomForestRegressor(CustomRandomForestClassifier):
    def __init__(self, x_dataset, y_dataset, sample_random_state, model_params):
        super().__init__(x_dataset, y_dataset, sample_random_state, model_params)
        self.model = RandomForestRegressor(**model_params)
        self.model_name = 'Random Forest Regressor'
    