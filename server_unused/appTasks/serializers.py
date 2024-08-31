from rest_framework import serializers
from .models import App, CompletedTask
from authentication.models import UserAccount

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['id', 'name', 'email', 'user_points']

# class UserAccountSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserAccount
#         fields = ['name', 'email', 'user_points']

class AppSerializer(serializers.ModelSerializer):
    class Meta:
        model = App
        fields = ['id', 'app_name', 'image', 'points', 'date_created']

class CompletedTaskSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    app = AppSerializer()
    class Meta:
        model = CompletedTask
        fields = ['id', 'user', 'app', 'screenshot', 'date_completed', 'verified']
        
class AddCompletedTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompletedTask
        fields = ['id','screenshot', 'date_completed', 'verified']
        
        
class CompletedTaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompletedTask
        fields = ['verified']