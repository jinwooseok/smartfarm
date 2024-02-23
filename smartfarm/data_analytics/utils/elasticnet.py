from sklearn.linear_model import ElasticNet
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd
import numpy as np

class CustomElasticNet:
    def __init__(self, x_dataset, y_dataset, random_state, alpha=1.0, l1_ratio=0.5):
        self.model = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=random_state)
        self.learned_model = None
        self.x_dataset = x_dataset
        self.y_dataset = y_dataset
        self.random_state = random_state
        self.alpha = alpha
        self.l1_ratio = l1_ratio
        self.model_name = 'ElasticNet'
        
    def fit(self):
        self.learned_model = self.model.fit(self.x_dataset, self.y_dataset)
        return self.learned_model
    
    def feature_importances(self):
        # ElasticNet has both L1 and L2 regularization, making it a combination of Lasso and Ridge.
        # You can extract feature coefficients as importances.
        importances = {
            f'Coefficient_{col}': coef
            for col, coef in zip(self.x_dataset.columns, self.learned_model.coef_)
        }
        return importances
    
    def meta(self):
        return {
            'model': self.model_name,
            'featureNames': list(self.x_dataset.columns),
            'targetNames': self.y_dataset.name,
            'randomState': self.random_state,
            'alpha': self.alpha,
            'l1_ratio': self.l1_ratio
        }
    
    def predict(self, x_test, y_test):
        y_pred = self.learned_model.predict(x_test)
        y_pred = np.round(y_pred, decimals=4)
        
        x_test = x_test.reset_index(drop=True)
        y_test = y_test.reset_index(drop=True)
        y_pred = pd.Series(y_pred, name=y_test.name + '_pred').reset_index(drop=True)
        
        # Evaluation
        mse = mean_sq
