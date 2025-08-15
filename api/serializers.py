from rest_framework import serializers
from .models import NeedPost, Response
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ResponseSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Response
        fields = '__all__'

class NeedPostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    responses = ResponseSerializer(many=True, read_only=True)
    
    class Meta:
        model = NeedPost
        fields = '__all__'