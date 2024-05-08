from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, confusion_matrix
import pandas as pd

class CustomNaiveBayes:
    def __init__(self, x_train, y_dataset, random_state):
        self.model = GaussianNB()
        self.learned_model = None
        self.x_train = x_train
        self.y_dataset = y_dataset
        self.random_state = random_state
        self.model_name = 'Naive Bayes'
        
    def fit(self):
        self.learned_model = self.model.fit(self.x_train, self.y_dataset)
        return self.learned_model
    
    def feature_importances(self):
        # Naive Bayes doesn't provide feature importances directly
        # You may want to add some custom logic based on the nature of your dataset
        
        # For example, you could calculate the mean and standard deviation for each feature for each class
        # and consider them as "importances"
        mean_by_class = self.x_train.groupby(self.y_dataset).mean()
        std_by_class = self.x_train.groupby(self.y_dataset).std()
        
        importances = {
            f'Mean_{col}_Class_{cls}': mean_by_class.loc[cls, col]
            for cls in mean_by_class.index
            for col in mean_by_class.columns
        }
        
        return importances
    
    def meta(self):
        return {
            'model': self.model_name,
            'featureNames': list(self.x_train.columns),
            'targetNames': self.y_dataset.name,
            'randomState': self.random_state
        }
    
    def predict(self, x_test, y_test):
        y_pred = self.learned_model.predict(x_test)
        
        x_test = x_test.reset_index(drop=True)
        y_test = y_test.reset_index(drop=True)
        y_pred = pd.Series(y_pred, name=y_test.name + '_pred').reset_index(drop=True)
        
        # Evaluation
        accuracy = accuracy_score(y_test, y_pred)
        confusion_mat = confusion_matrix(y_test, y_pred)
        
        # Additional results
        return {
            'model' : self.model_name,
            'featureNames': list(self.x_train.columns),
            'targetNames': self.y_dataset.name,
            'randomState': self.random_state,
            'Accuracy': round(accuracy, 4),
            'ConfusionMatrix': confusion_mat.tolist(),
            'testData': pd.concat([x_test, y_test, y_pred], axis=1).to_dict(orient='records'),
            'yPred': y_pred.tolist(),
            'y': y_test.tolist()
        }
