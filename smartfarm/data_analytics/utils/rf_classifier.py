from sklearn.ensemble import RandomForestClassifier

class CustomRandomForestClassifier():
    def __init__(self, x_dataset, y_dataset, n_estimators=100, random_state=42):
        self.model = RandomForestClassifier(n_estimators=n_estimators, random_state=random_state)
        self.learned_model = None
        self.x_dataset = x_dataset
        self.y_dataset = y_dataset
    
    def fit(self):
        self.learned_model = self.model.fit(self.x_dataset, self.y_dataset)
        return self.learned_model

    def feature_importances(self):
        return self.learned_model.feature_importances_
    
    def meta(self):
        return {
                'model_name' : 'Random Forest Classifier',
                'feature_names': list(self.x_dataset.columns),
                'target_names': self.y_dataset.name,
                'model_weights': self.learned_model.feature_importances_
            }