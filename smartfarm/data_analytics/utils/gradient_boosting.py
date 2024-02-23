from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd
import numpy as np

class CustomGradientBoosting:
    def __init__(self, x_dataset, y_dataset, random_state, n_estimators=100, learning_rate=0.1, max_depth=3):
        self.model = GradientBoostingRegressor(n_estimators=n_estimators, learning_rate=learning_rate, max_depth=max_depth, random_state=random_state)
        self.learned_model = None
        self.x_dataset = x_dataset
        self.y_dataset = y_dataset
        self.random_state = random_state
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.max_depth = max_depth
        self.model_name = 'Gradient Boosting'
        
    def fit(self):
        self.learned_model = self.model.fit(self.x_dataset, self.y_dataset)
        return self.learned_model
    
    def feature_importances(self):
        # Gradient Boosting provides feature importances based on the contribution of each feature to the model.
        importances = {
            f'Feature_{i}': importance
            for i, importance in enumerate(self.learned_model.feature_importances_)
        }
        return importances
    
    def meta(self):
        return {
            'model': self.model_name,
            'featureNames': list(self.x_dataset.columns),
            'targetNames': self.y_dataset.name,
            'randomState': self.random_state,
            'n_estimators': self.n_estimators,
            'learning_rate': self.learning_rate,
            'max_depth': self.max_depth
        }
    
    def predict(self, x_test, y_test):
        y_pred = self.learned_model.predict(x_test)
        y_pred = np.round(y_pred, decimals=4)
        
        x_test = x_test.reset_index(drop=True)
        y_test = y_test.reset_index(drop=True)
        y_pred = pd.Series(y_pred, name=y_test.name + '_pred').reset_index(drop=True)
        
        # Evaluation
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        # Additional results
        return {
            'model' : self.model_name,
            'featureNames': list(self.x_dataset.columns),
            'targetNames': self.y_dataset.name,
            'randomState': self.random_state,
            'n_estimators': self.n_estimators,
            'learning_rate': self.learning_rate,
            'max_depth': self.max_depth,
            'MSE': round(mse, 4),
            'R2': round(r2, 4),
            'testData': pd.concat([x_test, y_test, y_pred], axis=1).to_dict(orient='records'),
            'yPred': y_pred.tolist(),
            'y': y_test.tolist()
        }
