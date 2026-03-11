from rest_framework import serializers

from apps.users.models import Users
from helpers.helpers import (
    base64_to_image,
)




class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
    class Meta:
        model = Users
        fields = ['username','password']
        
    def validate(self, attrs):
        return super().validate(attrs)    



class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    


class RegisterUserSerializer(serializers.ModelSerializer):
    username            = serializers.CharField(required=True)
    email               = serializers.EmailField(required=True)
    password            = serializers.CharField(required=True)
    confirm_password    = serializers.CharField(required=True,write_only=True)
    image               = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = Users
        fields = ['username', 'email', 'password','confirm_password','image']

    def validate(self, attrs):
        if Users.objects.filter(username=attrs.get('username')).exists():
            raise serializers.ValidationError("Username already exists.")
        
        if Users.objects.filter(email=attrs.get('email')).exists():
            raise serializers.ValidationError("Email already exists.")
        
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError("Password and Confirm Password do not match.")
        
        return super().validate(attrs)

    def create(self, validated_data):

        validated_data.pop('confirm_password',None)
        password       = validated_data.pop('password',None)
        user           = Users()
        user.username  = validated_data.get('username','')
        user.email     = validated_data.get('email','') 


        base64_image = validated_data.pop('image',None)
        if base64_image:
            image_file   = base64_to_image(base64_image)
            user.image = image_file

        if password:
            user.set_password(password)

        user.save()

        return user


        