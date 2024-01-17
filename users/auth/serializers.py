from rest_framework import serializers
from ..models import User
class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user_id",required=True)
    password = serializers.CharField(source="user_pw",required=True)
    name = serializers.CharField(source="user_name",required=True)
    job = serializers.CharField(source="user_job",required=True)
    phone = serializers.ListField(source="user_phone",required=True)
    class Meta:
        model = User
        write_only=True
        fields = ['email', 'password', 'name', 'job', 'phone']   
    
class EmailValidationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

class SignInSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
