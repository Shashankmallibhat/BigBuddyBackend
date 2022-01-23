from rest_framework import serializers
from django.conf import settings
import uuid
from django.contrib.auth import get_user_model

from authentication.models import ProfileData

UserModel = get_user_model()

class SignUPSerializer(serializers.ModelSerializer):
    
    confirmPassword = serializers.CharField(style={'input_type': 'password'},write_only=True)
    class Meta:
        model = UserModel
        fields = ['username', 'email', 'password', 'confirmPassword','role']
        extra_kwargs = {
            'password': {'write_only': True}
            }
        
    def create(self, validated_data):
        usercode = uuid.uuid4()
        user = UserModel.objects.create_user(username=self.validated_data['username'], password=self.validated_data['password'], email=self.validated_data['email'],role=self.validated_data['role'],usercode=usercode)
        return user 
       
    def save(self):
        password = self.validated_data['password']
        confirmPassword = self.validated_data['confirmPassword']
     
        if password != confirmPassword:
            raise serializers.ValidationError({'error': 'password and confirmPassword are not same'})
        
        if UserModel.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({'error': 'Email already exists'})
        
        if UserModel.objects.filter(username=self.validated_data['username']).exists():
            raise serializers.ValidationError({'error': 'username already exists'})
        
        usercode = uuid.uuid4()
        account = UserModel.objects.create_user(username=self.validated_data['username'], password=self.validated_data['password'], email=self.validated_data['email'],role=self.validated_data['role'],usercode=usercode)
        
        return account
    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileData
        fields = ['username', 'email','role','description','avatarURL']