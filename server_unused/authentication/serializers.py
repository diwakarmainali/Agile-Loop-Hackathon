from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import UserAccount
from appTasks.models import App
from appTasks.serializers import AppSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.name
        token['email'] = user.email

        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        # Add user profile info to the response
        data['user'] = {
            'name': user.name,
            'email': user.email,
            'user_points': user.user_points,
            'admin':user.is_staff
        }

        # Add registered apps to the response
        apps = App.objects.filter()
        data['apps'] = AppSerializer(apps, many=True).data

        return data

class RegisterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        required=True,
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=UserAccount.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    

    class Meta:
        model = UserAccount
        fields = ('name','email', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = UserAccount.objects.create(
            name=validated_data['name'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()

        

        return user
        

