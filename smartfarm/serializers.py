from rest_framework import serializers
from .models import File
from users.models import User

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['user_id', 'file_title', 'file_root', 'created_at', 'updated_at']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_name','user_id','user_pw']

    