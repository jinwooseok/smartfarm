from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
class CustomRandomForestClassifier():
    def __init__(self, x_dataset, y_dataset, n_estimators=100, random_state=42):
        self.model = RandomForestClassifier(n_estimators=n_estimators, random_state=random_state)
        self.learned_model = None
        self.x_dataset = x_dataset
        self.y_dataset = y_dataset
        self.random_state = random_state
        self.params = {
            'n_estimators':(100, 200),
            'max_depth' : (5, 8),
            'min_samples_leaf' : (8, 18),
            'min_samples_split' : (8, 16)
        }
        self.model_name = 'Random Forest Classifier'
    
    def fit(self):
        self.learned_model = self.model.fit(self.x_dataset, self.y_dataset)
        return self.learned_model

    def feature_importances(self):
        return self.learned_model.feature_importances_
    
    def meta(self):
        return {
                'model_name' : self.model_name,
                'feature_names': list(self.x_dataset.columns),
                'target_names': self.y_dataset.name,
                'model_weights': self.learned_model.feature_importances_,
                'random_state': self.random_state
            }
    
class CustomRandomForestRegressor(CustomRandomForestClassifier):
    def __init__(self, x_dataset, y_dataset, n_estimators=100, random_state=42):
        super().__init__(x_dataset, y_dataset, n_estimators, random_state)
        self.model = RandomForestRegressor(n_estimators=n_estimators, random_state=random_state)
        self.model_name = 'Random Forest Regressor'
    def fit(self):
        grid_cv = GridSearchCV(self.model, param_grid=self.params, cv=2, n_jobs=-1)
        grid_cv.fit(self.x_dataset, self.y_dataset)
    