from rest_framework import serializers
from ..file.serializers import FileNameSerializer
from ..models import LearnedModel
from ..file.exceptions.file_exception import FileNotFoundException
class CreateModelSerializer(FileNameSerializer):
    modelName = serializers.CharField()
    xValue = serializers.JSONField()
    yValue = serializers.CharField()
    trainSize = serializers.FloatField()
    fileData = serializers.JSONField()
    modelParams = serializers.JSONField(required=False, default={})
    model = serializers.ChoiceField(choices=[("linear","linear")
                                             ,("logistic","logistic")
                                             ,("ridge","ridge")
                                             ,("lasso","lasso")
                                             ,("elastic","elastic")
                                             ,("decision","decision")
                                             ,("rf","rf")
                                             ,("rfr","rfr")
                                             ,("gb","gb")
                                             ,("ada","ada")
                                             ,("xgb","xgb")
                                             ,("lightgbm","lightgbm")
                                             ,("catboost","catboost")
                                             ,("svc","svc")
                                             ,("svr","svr")
                                             ,("elastic","elastic")
                                             ,("naive","naive")])

class RidgeSerializer(serializers.Serializer):
    random_state = serializers.IntegerField(default=42, required=False)
    alpha = serializers.FloatField(default=1.0, required=False)
    
class LassoSerializer(serializers.Serializer):
    random_state = serializers.IntegerField(default=42, required=False)
    alpha = serializers.FloatField(default=1.0, required=False)

class ElasticSerializer(serializers.Serializer):
    random_state = serializers.IntegerField(default=42, required=False)
    alpha = serializers.FloatField(default=1.0, required=False)
    l1_ratio = serializers.FloatField(default=0.5, required=False)

class SVMSerializer(serializers.Serializer):
    kernel = serializers.ChoiceField(choices=["linear", "poly", "rbf", "sigmoid"], default="rbf", required=False)

class RFRegressorSerializer(serializers.Serializer):
    n_estimators = serializers.IntegerField(default=100, required=False)
    max_depth = serializers.IntegerField(default=3, required=False)

class RFClassifierSerializer(serializers.Serializer):
    n_estimators = serializers.IntegerField(default=100, required=False)
    max_depth = serializers.IntegerField(default=3, required=False)

class GBRegressorSerializer(serializers.Serializer):
    n_estimators = serializers.IntegerField(default=100, required=False)
    learning_rate = serializers.FloatField(default=0.1, required=False)
    max_depth = serializers.IntegerField(default=3, required=False)


class ModelNameSerializer(serializers.Serializer):
    modelName = serializers.CharField()
    
    def get_model_object(self, user)->LearnedModel:
        try:
            return LearnedModel.objects.get(user=user, model_name=self.data['modelName'])
        except LearnedModel.DoesNotExist:
            raise FileNotFoundException()
        
class PredictModelSerializer(ModelNameSerializer):
    testData = serializers.JSONField()
    xValue = serializers.CharField()
    yValue = serializers.CharField()