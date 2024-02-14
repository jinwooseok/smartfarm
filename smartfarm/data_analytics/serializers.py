from rest_framework import serializers
from ..file.serializers import FileNameSerializer
class CreateModelSerializer(FileNameSerializer):
    modelName = serializers.CharField()
    xValue = serializers.JSONField()
    yValue = serializers.CharField()
    trainSize = serializers.FloatField()
    model = serializers.ChoiceField(choices=[("linear","linear"),("ridge","ridge"),("lasso","lasso"),("elastic","elastic"),("decision","decision"),("random","random"),("gradient","gradient"),("adaboost","adaboost"),("xgboost","xgboost"),("lightgbm","lightgbm"),("catboost","catboost")])
