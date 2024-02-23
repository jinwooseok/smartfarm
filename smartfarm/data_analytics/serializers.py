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
    isSave = serializers.BooleanField(default=False, required=False)
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