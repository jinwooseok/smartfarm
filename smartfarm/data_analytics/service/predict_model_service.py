from ..utils.rf_classifier import CustomRandomForestClassifier
from ..utils.linear import CustomLinearRegression
import pickle
class PredictModelService:
    def __init__(self, model_object, test_data, x_value, y_value):
        self.model_object = model_object
        self.test_data = test_data
        self.x_value = x_value
        self.y_value = y_value
        self.loaded_model = None
    
    def from_serializer(cls, serializer, user) -> "PredictModelService":
        return cls(serializer.get_model_object(user)
                   ,serializer.validated_data['testData']
                   ,serializer.validated_data['xValue']
                   ,serializer.validated_data['yValue'])
    
    def execute(self):
        x_test = self.test_data[self.x_value]
        y_test = self.test_data[self.y_value]
        self.loaded_model = self.load_model()
        result = self.model_handler(x_test, y_test)
        return result
        
        
    def model_handler(self, x_df, y_df, random_state=42):
        if self.model == "linear":
            model = CustomLinearRegression(x_df, y_df, random_state)
            model.learned_model = self.loaded_model
            result = model.predict(x_df, y_df)
            return result
    
    def load_model(self):
        model = pickle.load(self.model_object)        
        return model