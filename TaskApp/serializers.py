from rest_framework import serializers
from .models import Task, User
from django.contrib.auth import authenticate


class TaskSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    class Meta:
        model = Task
        fields = ('id', 'Title', 'Description', 'Date', 'Completed', 'user')


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email', 'password']
#         extra_kwargs = {'password': {'write_only': True}}  # Make password write-only

#     def create(self, validated_data):
#         user = User.objects.create_user(
#             username=validated_data['username'],
#             email=validated_data['email'],
#             password=validated_data['password']
#         )
#         return user
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},  # This hides the password in responses
            'email': {'required': True},       # Ensures email is required
        }

    def create(self, validated_data):
        # Use `set_password` to hash the password before saving
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                attrs['user'] = user
            else:
                raise serializers.ValidationError('Invalid username or password.')
        else:
            raise serializers.ValidationError('Must include "username" and "password".')
        return attrs
    
# class UserLoginSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField()
    
# class UserRegistrationSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password']

#     def create(self, validated_data):
#         user = User(
#             username=validated_data['username'],
#             email=validated_data['email'],
#         )
#         user.set_password(validated_data['password'])  # Use set_password to hash the password
#         user.save()
#         return user
    
