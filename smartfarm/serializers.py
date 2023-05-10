from rest_framework import serializers
from .models import File_db
from users.models import User

class FileSerializer(serializers.Serializer):
    class Meta:
        model = File_db
        fields = ['url', 'user_id', 'file_Title', 'file_Root', 'created_at', 'updated_at']

class UserSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ['url','user_name','user_email']

    