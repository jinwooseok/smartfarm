from sklearn.ensemble import RandomForestClassifier

class CustomRandomForestClassifier():
    def __init__(self, n_estimators=100, random_state=42):
        self.model = RandomForestClassifier(n_estimators=n_estimators, random_state=random_state)
        self.learned_model = None
    
    def fit(self, X, y):
        self.learned_model = self.model.fit(X, y)

    def feature_importances(self):
        return self.learned_model.feature_importances_