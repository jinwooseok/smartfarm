from sklearn.ensemble import RandomForestClassifier

class CustomRandomForestClassifier():
    def __init__(self, n_estimators=100, random_state=42):
        self.model = RandomForestClassifier(n_estimators=n_estimators, random_state=random_state)
        self.learned_model = None
    
    def fit(self, x_dataset, y_dataset):
        self.learned_model = self.model.fit(x_dataset, y_dataset)
        return self.learned_model

    def feature_importances(self):
        return self.learned_model.feature_importances_